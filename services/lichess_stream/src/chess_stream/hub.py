"""Per-game streaming sessions, subscriber fan-out, and broadcast."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional, Set

from .config import Settings
from .lichess import FatalStreamError, LichessStreamClient, TransientStreamError
from .schema import BoardStateValidator, SchemaValidationError
from .tracker import BoardTracker, TrackerError

logger = logging.getLogger(__name__)

_ONGOING_STATUSES = {"created", "started"}


def _status_name(status: Any) -> Optional[str]:
    if isinstance(status, dict):
        name = status.get("name")
        return name if isinstance(name, str) else None
    if isinstance(status, str):
        return status
    return None


class Subscriber:
    """A single WebSocket client with a bounded, latest-wins message queue."""

    def __init__(self, queue_size: int) -> None:
        self.queue: asyncio.Queue[Dict[str, Any]] = asyncio.Queue(maxsize=queue_size)

    def offer(self, message: Dict[str, Any]) -> None:
        try:
            self.queue.put_nowait(message)
        except asyncio.QueueFull:
            try:
                self.queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            try:
                self.queue.put_nowait(message)
            except asyncio.QueueFull:
                pass

    async def get(self) -> Dict[str, Any]:
        return await self.queue.get()


class GameSession:
    """Owns the Lichess stream for one game and the board tracker derived from it."""

    def __init__(
        self, game_id: str, settings: Settings, validator: Optional[BoardStateValidator]
    ) -> None:
        self.game_id = game_id
        self._settings = settings
        self._validator = validator
        self._tracker = BoardTracker(
            game_id, max_processed_events=settings.max_processed_events
        )
        self._initialized = False
        self._subscribers: Set[Subscriber] = set()
        self._task: Optional[asyncio.Task[None]] = None
        self._lock = asyncio.Lock()
        self._last_snapshot: Optional[Dict[str, Any]] = None
        self._last_game_info: Optional[Dict[str, Any]] = None
        self._terminal_message: Optional[Dict[str, Any]] = None
        self._closed = False

    @property
    def subscriber_count(self) -> int:
        return len(self._subscribers)

    def current_state(self) -> Dict[str, Any]:
        if self._last_snapshot is not None:
            return self._last_snapshot
        return self._tracker.snapshot()

    async def add_subscriber(self, subscriber: Subscriber) -> None:
        async with self._lock:
            self._subscribers.add(subscriber)
            if self._last_game_info is not None:
                subscriber.offer(self._last_game_info)
            if self._last_snapshot is not None:
                subscriber.offer(
                    {
                        "type": "snapshot",
                        "game_id": self.game_id,
                        "state": self._last_snapshot,
                    }
                )
            if self._terminal_message is not None:
                subscriber.offer(self._terminal_message)
            if self._task is None or self._task.done():
                self._closed = False
                self._terminal_message = None
                self._task = asyncio.create_task(
                    self._run(), name=f"stream:{self.game_id}"
                )

    async def remove_subscriber(self, subscriber: Subscriber) -> bool:
        async with self._lock:
            self._subscribers.discard(subscriber)
            if self._subscribers:
                return False
            self._closed = True
            if self._task is not None:
                self._task.cancel()
                self._task = None
            return True

    def _broadcast(self, message: Dict[str, Any]) -> None:
        for subscriber in list(self._subscribers):
            subscriber.offer(message)

    def _validate(self, state: Dict[str, Any]) -> None:
        if self._validator is None or not self._settings.validate_snapshots:
            return
        try:
            self._validator.validate(state)
        except SchemaValidationError as exc:
            logger.error("game %s produced an invalid snapshot: %s", self.game_id, exc)
            raise

    def _publish_snapshot(self, message_type: str) -> None:
        state = self._tracker.snapshot()
        self._validate(state)
        self._last_snapshot = state
        self._broadcast({"type": message_type, "game_id": self.game_id, "state": state})

    def _handle_description(self, data: Dict[str, Any]) -> bool:
        fen = data.get("fen")
        info = {
            "type": "game_info",
            "game_id": self.game_id,
            "status": _status_name(data.get("status")),
            "variant": data.get("variant"),
            "speed": data.get("speed"),
            "rated": data.get("rated"),
            "players": data.get("players"),
            "fen": fen,
            "winner": data.get("winner"),
        }
        self._last_game_info = info
        self._broadcast(info)

        if isinstance(fen, str):
            placement = fen.split(" ", 1)[0]
            if not self._initialized:
                self._tracker.reset_from_fen(fen)
                self._initialized = True
                self._publish_snapshot("snapshot")
            elif self._tracker.board.board_fen() != placement:
                self._tracker.reset_from_fen(fen)
                self._publish_snapshot("resync")

        status_name = _status_name(data.get("status"))
        if status_name is not None and status_name not in _ONGOING_STATUSES:
            terminal = {
                "type": "game_over",
                "game_id": self.game_id,
                "status": status_name,
                "winner": data.get("winner"),
            }
            self._terminal_message = terminal
            self._broadcast(terminal)
            return True
        return False

    def _handle_move(self, data: Dict[str, Any]) -> None:
        fen = data.get("fen")
        if not isinstance(fen, str):
            return
        placement = fen.split(" ", 1)[0]

        if not self._initialized:
            self._tracker.reset_from_fen(fen)
            self._initialized = True
            self._publish_snapshot("snapshot")
            return

        if self._tracker.board.board_fen() == placement:
            return

        uci = data.get("lm")
        if not isinstance(uci, str) or not uci:
            uci = self._tracker.infer_uci_from_fen(fen)
        if not uci:
            self._tracker.reset_from_fen(fen)
            self._publish_snapshot("resync")
            return

        try:
            event = self._tracker.apply_uci(uci)
        except TrackerError as exc:
            logger.warning(
                "game %s move %s could not be applied (%s); resyncing",
                self.game_id,
                uci,
                exc,
            )
            self._tracker.reset_from_fen(fen)
            self._publish_snapshot("resync")
            return

        if self._tracker.board.board_fen() != placement:
            self._tracker.reset_from_fen(fen)
            self._publish_snapshot("resync")
            return

        state = self._tracker.snapshot()
        self._validate(state)
        self._last_snapshot = state
        clocks = {key: data[key] for key in ("wc", "bc") if key in data}
        message = {
            "type": "move",
            "game_id": self.game_id,
            "move": event,
            "state": state,
        }
        if clocks:
            message["clocks"] = clocks
        self._broadcast(message)

    def _dispatch(self, data: Dict[str, Any]) -> bool:
        is_description = "players" in data or ("id" in data and "variant" in data)
        if is_description:
            return self._handle_description(data)
        if "fen" in data:
            self._handle_move(data)
        return False

    async def _run(self) -> None:
        delay = self._settings.reconnect_initial_delay
        client = LichessStreamClient(
            base_url=self._settings.lichess_base_url,
            token=self._settings.lichess_token,
            connect_timeout=self._settings.lichess_connect_timeout,
        )
        try:
            while not self._closed:
                try:
                    game_over = False
                    async for message in client.stream_game(self.game_id):
                        if self._dispatch(message):
                            game_over = True
                            break
                    if game_over:
                        return
                    delay = self._settings.reconnect_initial_delay
                except asyncio.CancelledError:
                    raise
                except FatalStreamError as exc:
                    logger.info("game %s fatal stream error: %s", self.game_id, exc)
                    self._terminal_message = {
                        "type": "error",
                        "game_id": self.game_id,
                        "fatal": True,
                        "message": str(exc),
                    }
                    self._broadcast(self._terminal_message)
                    return
                except TransientStreamError as exc:
                    logger.warning(
                        "game %s transient stream error: %s", self.game_id, exc
                    )
                    self._broadcast(
                        {
                            "type": "error",
                            "game_id": self.game_id,
                            "fatal": False,
                            "message": str(exc),
                        }
                    )
                if self._closed:
                    return
                await asyncio.sleep(delay)
                delay = min(delay * 2, self._settings.reconnect_max_delay)
        finally:
            await client.aclose()


class GameHub:
    """Registry of active game sessions."""

    def __init__(
        self, settings: Settings, validator: Optional[BoardStateValidator]
    ) -> None:
        self._settings = settings
        self._validator = validator
        self._sessions: Dict[str, GameSession] = {}
        self._lock = asyncio.Lock()

    async def subscribe(self, game_id: str) -> tuple[GameSession, Subscriber]:
        subscriber = Subscriber(self._settings.subscriber_queue_size)
        async with self._lock:
            session = self._sessions.get(game_id)
            if session is None:
                session = GameSession(game_id, self._settings, self._validator)
                self._sessions[game_id] = session
        await session.add_subscriber(subscriber)
        return session, subscriber

    async def unsubscribe(self, game_id: str, subscriber: Subscriber) -> None:
        async with self._lock:
            session = self._sessions.get(game_id)
        if session is None:
            return
        empty = await session.remove_subscriber(subscriber)
        if empty:
            async with self._lock:
                current = self._sessions.get(game_id)
                if current is session and current.subscriber_count == 0:
                    del self._sessions[game_id]

    def active_games(self) -> List[str]:
        return sorted(self._sessions)

    async def shutdown(self) -> None:
        async with self._lock:
            sessions = list(self._sessions.values())
            self._sessions.clear()
        for session in sessions:
            session._closed = True
            if session._task is not None:
                session._task.cancel()
        for session in sessions:
            task = session._task
            if task is not None:
                try:
                    await task
                except (asyncio.CancelledError, Exception):
                    pass
