from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import Any, Iterable, Optional, Tuple
import json
import re

from .errors import ConfigurationError, GantryError, PlanningError, ValidationError
from .lichess_pgn import fetch_pgn, lichess_client, pgn_moves
from .models import BoardState, MoveDelta
from .persistence import atomic_write_json, read_json
from .service import GantryService


_RESULT_RE = re.compile(r'^\[Result\s+"([^"]+)"\]\s*$', re.MULTILINE)


def _game_is_finished(pgn: str) -> bool:
    match = _RESULT_RE.search(pgn)
    return match is not None and match.group(1) in {"1-0", "0-1", "1/2-1/2"}


@dataclass(frozen=True)
class FollowSession:
    game_id: str
    base_state: BoardState
    emitted_event_ids: frozenset[str]

    @classmethod
    def load_or_create(
        cls, path: Path, game_id: str, state: BoardState, reset: bool
    ) -> "FollowSession":
        if path.exists() and not reset:
            raw = read_json(path)
            if raw.get("game_id") != game_id:
                raise ConfigurationError(
                    f"session {path} belongs to another game; use --reset-session"
                )
            base = BoardState.from_mapping(raw.get("base_state", {}))
            emitted = raw.get("emitted_event_ids", [])
            if not isinstance(emitted, list) or not all(
                isinstance(item, str) for item in emitted
            ):
                raise ValidationError(
                    "Lichess follow session has invalid emitted_event_ids"
                )
            return cls(game_id, base, frozenset(emitted))
        return cls(game_id, state, frozenset())

    def save(self, path: Path) -> None:
        atomic_write_json(
            path,
            {
                "schema_version": 1,
                "game_id": self.game_id,
                "base_state": self.base_state.to_dict(),
                "emitted_event_ids": sorted(self.emitted_event_ids),
            },
        )

    def with_emitted(self, event_id: str) -> "FollowSession":
        return FollowSession(
            self.game_id,
            self.base_state,
            self.emitted_event_ids | {event_id},
        )


def _write_plan(output_dir: Path, move: MoveDelta, program_text: str) -> None:
    (output_dir / f"{move.event_id}.json").write_text(
        json.dumps(move.to_dict(), indent=2, sort_keys=True) + "\n", encoding="ascii"
    )
    (output_dir / f"{move.event_id}.gcode").write_text(program_text, encoding="ascii")


def _state_before(
    moves: Iterable[MoveDelta],
    target: MoveDelta,
    base: BoardState,
    service: GantryService,
) -> BoardState:
    state = base
    for move in moves:
        if move.event_id == target.event_id:
            return state
        plan = service.plan(move, state)
        state = plan.next_state
    raise ValidationError(
        f"Lichess move {target.event_id} is missing from its PGN sequence"
    )


def _process_available(
    service: GantryService,
    game_id: str,
    output_dir: Path,
    session_path: Path,
    session: FollowSession,
    *,
    execute: bool,
    execute_existing: bool,
    token: Optional[str],
    client: Any,
) -> Tuple[FollowSession, bool]:
    pgn = fetch_pgn(game_id, token=token, client=client)
    moves = tuple(pgn_moves(game_id, pgn, session.base_state))
    for move in moves:
        assert move.event_id is not None
        already_emitted = move.event_id in session.emitted_event_ids
        already_executed = move.event_id in service.store.load().processed_events
        if execute:
            if already_executed:
                continue
            if already_emitted and not execute_existing:
                continue
            plan = service.execute(move)
            _write_plan(output_dir, move, plan.program.text())
            print(
                f"\n; executed Lichess move {move.event_id}\n{plan.program.text()}",
                end="",
            )
        else:
            if already_emitted:
                continue
            try:
                plan = service.plan(
                    move, _state_before(moves, move, session.base_state, service)
                )
            except PlanningError as exc:
                raise PlanningError(
                    f"Lichess move {move.event_id} ({move.piece_id}: "
                    f"{move.previous.x},{move.previous.y} -> "
                    f"{move.new.x},{move.new.y}) failed: {exc}"
                ) from exc
            _write_plan(output_dir, move, plan.program.text())
            print(
                f"\n; dry-run Lichess move {move.event_id}\n{plan.program.text()}",
                end="",
            )
        session = session.with_emitted(move.event_id)
        session.save(session_path)
    return session, _game_is_finished(pgn)


def follow_game(
    service: GantryService,
    game_id: str,
    output_dir: Path,
    session_path: Path,
    *,
    interval_s: float,
    execute: bool,
    execute_existing: bool,
    reset_session: bool,
    once: bool,
    token: Optional[str] = None,
) -> None:
    if interval_s <= 0:
        raise ConfigurationError("reconnect interval must be positive")
    if service.journal.exists():
        raise ConfigurationError(
            f"pending transaction exists at {service.journal.path}; reconcile it first"
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    session = FollowSession.load_or_create(
        session_path, game_id, service.store.load(), reset_session
    )
    session.save(session_path)
    client = lichess_client(token)
    print(
        f"Following Lichess game {game_id} in real time; "
        f"{'executing' if execute else 'dry-running'} new moves. Files: {output_dir}"
    )

    session, finished = _process_available(
        service,
        game_id,
        output_dir,
        session_path,
        session,
        execute=execute,
        execute_existing=execute_existing,
        token=token,
        client=client,
    )
    if finished:
        service.finish_game()
        return
    if once:
        return

    while True:
        try:
            for _event in client.games.stream_game_moves(game_id):
                session, finished = _process_available(
                    service,
                    game_id,
                    output_dir,
                    session_path,
                    session,
                    execute=execute,
                    execute_existing=execute_existing,
                    token=token,
                    client=client,
                )
                if finished:
                    service.finish_game()
                    return
        except GantryError:
            raise
        except Exception as exc:
            print(
                f"\n; Lichess stream interrupted ({exc}); "
                f"reconnecting in {interval_s:g}s",
                end="",
            )
            sleep(interval_s)
            continue
        session, finished = _process_available(
            service,
            game_id,
            output_dir,
            session_path,
            session,
            execute=execute,
            execute_existing=execute_existing,
            token=token,
            client=client,
        )
        if finished:
            service.finish_game()
            return
        sleep(interval_s)
