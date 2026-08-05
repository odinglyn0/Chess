from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil
import threading
from typing import Any, Callable, Optional

from .config import AppConfig
from .errors import ConfigurationError, ValidationError
from .lichess_pgn import fetch_pgn, lichess_client, pgn_moves
from .models import BoardState
from .persistence import atomic_write_json
from .service import GantryService
from .serial_link import MarlinSerial


GAME_ID_RE = re.compile(r"^[A-Za-z0-9]{8,12}$")


@dataclass(frozen=True)
class LiveGameStatus:
    state: str
    game_id: Optional[str]
    started_at: Optional[str]
    last_event_id: Optional[str]
    executed_count: int
    error: Optional[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "game_id": self.game_id,
            "started_at": self.started_at,
            "last_event_id": self.last_event_id,
            "executed_count": self.executed_count,
            "error": self.error,
        }


class LiveGameManager:
    def __init__(
        self,
        root: Path,
        config: AppConfig,
        *,
        demo: bool,
        service_factory: Optional[Callable[..., GantryService]] = None,
        client_factory: Callable[[Optional[str]], Any] = lichess_client,
        pgn_fetcher: Callable[..., str] = fetch_pgn,
    ) -> None:
        self.root = root
        self.config = config
        self.demo = demo
        self._service_factory = service_factory or GantryService
        self._client_factory = client_factory
        self._pgn_fetcher = pgn_fetcher
        self._lock = threading.RLock()
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._service: Optional[GantryService] = None
        self._link: Optional[MarlinSerial] = None
        self._status = LiveGameStatus("idle", None, None, None, 0, None)
        self._logs = ""
        self._run_number = 0

    def status(self) -> dict[str, Any]:
        with self._lock:
            return {"status": self._status.as_dict(), "logs": self._logs}

    def running(self) -> bool:
        with self._lock:
            return self._status.state in {
                "starting",
                "homing",
                "following",
                "executing",
            }

    def _append(self, line: str) -> None:
        with self._lock:
            stamp = datetime.now().strftime("%H:%M:%S")
            self._logs = (self._logs + f"[{stamp}] {line}\n")[-100_000:]

    def _set(self, **changes: Any) -> None:
        with self._lock:
            values = self._status.as_dict()
            values.update(changes)
            self._status = LiveGameStatus(**values)

    def start(
        self,
        game_id: str,
        *,
        confirm_standard_position: bool,
        confirm_motion: bool,
        token: Optional[str] = None,
    ) -> dict[str, Any]:
        game_id = game_id.strip()
        if not GAME_ID_RE.fullmatch(game_id):
            raise ValidationError("Lichess game ID must contain 8-12 letters or digits")
        if not confirm_standard_position:
            raise ValidationError(
                "confirm that the physical board is in the standard position"
            )
        if not self.demo and not confirm_motion:
            raise ValidationError(
                "physical live play requires explicit motion confirmation"
            )
        with self._lock:
            if self.running():
                raise ConfigurationError("a live Lichess game is already running")
            self._run_number += 1
            self._stop.clear()
            self._logs = ""
            self._status = LiveGameStatus(
                "starting",
                game_id,
                datetime.now(timezone.utc).isoformat(),
                None,
                0,
                None,
            )
            self._thread = threading.Thread(
                target=self._run,
                args=(game_id, token),
                daemon=True,
            )
            self._thread.start()
        return self.status()

    def _fresh_service(self, game_id: str) -> GantryService:
        path = self.root / "data" / "web-live" / f"run-{self._run_number}-{game_id}"
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
        state_path = path / "board_state.json"
        journal_path = path / "pending_move.json"
        audit_path = path / "audit.jsonl"
        atomic_write_json(state_path, BoardState.standard().to_dict())
        return self._service_factory(
            self.config,
            state_path,
            journal_path,
            audit_path,
        )

    def _run(self, game_id: str, token: Optional[str]) -> None:
        try:
            service = self._fresh_service(game_id)
            self._service = service
            client = self._client_factory(token)
            pgn = self._pgn_fetcher(game_id, token=token, client=client)
            baseline = tuple(pgn_moves(game_id, pgn, BoardState.standard()))
            if baseline:
                raise ConfigurationError(
                    "the game already has moves; start the TV follower before White's first move"
                )
            seen = {move.event_id for move in baseline if move.event_id is not None}
            self._append(
                f"Connected to {game_id}; ignoring {len(seen)} move event(s) already present at Start."
            )
            if self.demo:
                self._follow_stream(service, client, game_id, token, seen, None)
            else:
                link = MarlinSerial(self.config.serial)
                self._link = link
                with link:
                    self._set(state="homing")
                    self._append("Homing gantry once before live play.")
                    service.home_with_link(link)
                    self._follow_stream(service, client, game_id, token, seen, link)
            self._set(state="stopped" if self._stop.is_set() else "finished")
            self._append(
                "Live game follower stopped."
                if self._stop.is_set()
                else "Game stream finished."
            )
        except Exception as exc:
            self._append(f"Live game failed: {exc}")
            self._set(state="failed", error=str(exc))
        finally:
            self._link = None
            self._service = None

    def _follow_stream(
        self,
        service: GantryService,
        client: Any,
        game_id: str,
        token: Optional[str],
        seen: set[str],
        link: Optional[MarlinSerial],
    ) -> None:
        self._set(state="following")
        self._append("Waiting for new Lichess moves via the streaming API.")
        for _event in client.games.stream_game_moves(game_id):
            if self._stop.is_set():
                return
            pgn = self._pgn_fetcher(game_id, token=token, client=client)
            moves = tuple(pgn_moves(game_id, pgn, BoardState.standard()))
            for move in moves:
                if (
                    self._stop.is_set()
                    or move.event_id is None
                    or move.event_id in seen
                ):
                    continue
                if move.capture is not None and not self.config.capture.enabled:
                    raise ConfigurationError(
                        f"Lichess move {move.event_id} is a capture, but physical capture slots are disabled"
                    )
                self._set(state="executing")
                self._append(
                    f"Executing {move.event_id}: {move.piece_id} "
                    f"{move.previous.x},{move.previous.y} -> {move.new.x},{move.new.y}"
                )
                if self.demo:
                    state = service.store.load()
                    plan = service.plan(move, state)
                    service.store.save(plan.next_state)
                else:
                    assert link is not None
                    service.execute_with_link(move, link)
                seen.add(move.event_id)
                self._set(
                    last_event_id=move.event_id,
                    executed_count=self._status.executed_count + 1,
                    state="following",
                )

    def stop(self) -> dict[str, Any]:
        with self._lock:
            if not self.running():
                raise ConfigurationError("there is no running live game")
            self._stop.set()
            service = self._service
            link = self._link
            thread = self._thread
        if service is not None and link is not None and not self.demo:
            try:
                service.emergency_stop_with_link(link)
                self._append("Emergency stop sent while stopping physical live play.")
            except Exception as exc:
                self._append(f"Emergency stop attempt failed: {exc}")
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=3)
        self._set(state="stopped")
        return self.status()
