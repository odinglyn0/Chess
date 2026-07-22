from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import Any, Iterable, Mapping
import json

from .errors import ConfigurationError, PlanningError, ValidationError
from .lichess_pgn import fetch_pgn, pgn_moves
from .models import BoardState, MoveDelta
from .persistence import atomic_write_json, read_json
from .service import GantryService


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


def _write_plan(output_dir: Path, move: MoveDelta, program_text: str) -> None:
    (output_dir / f"{move.event_id}.json").write_text(
        json.dumps(move.to_dict(), indent=2, sort_keys=True) + "\n", encoding="ascii"
    )
    (output_dir / f"{move.event_id}.gcode").write_text(program_text, encoding="ascii")


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
) -> None:
    if interval_s <= 0:
        raise ConfigurationError("poll interval must be positive")
    if service.journal.exists():
        raise ConfigurationError(
            f"pending transaction exists at {service.journal.path}; reconcile it first"
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    session = FollowSession.load_or_create(
        session_path, game_id, service.store.load(), reset_session
    )
    session.save(session_path)
    print(
        f"Following Lichess game {game_id}; {'executing' if execute else 'dry-running'} "
        f"every {interval_s:g}s. Files: {output_dir}"
    )
    while True:
        pgn = fetch_pgn(game_id)
        moves = tuple(pgn_moves(game_id, pgn, session.base_state))
        for move in moves:
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
                        f"{move.previous.x},{move.previous.y} -> {move.new.x},{move.new.y}) failed: {exc}"
                    ) from exc
                _write_plan(output_dir, move, plan.program.text())
                print(
                    f"\n; dry-run Lichess move {move.event_id}\n{plan.program.text()}",
                    end="",
                )
            session = FollowSession(
                session.game_id,
                session.base_state,
                session.emitted_event_ids | {move.event_id},
            )
            session.save(session_path)
        if once:
            return
        sleep(interval_s)


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
