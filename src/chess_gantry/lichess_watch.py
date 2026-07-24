from __future__ import annotations

import asyncio
import json
from pathlib import Path

from .errors import ConfigurationError, PendingTransactionError, ValidationError
from .lichess_adapter import stream_event_to_move
from .service import GantryService


async def watch_game(
    service: GantryService,
    stream_url: str,
    game_id: str,
    output_dir: Path,
    *,
    execute: bool,
) -> None:
    try:
        from websockets.asyncio.client import connect
    except ImportError as exc:
        raise ConfigurationError("websockets is not installed; run 'uv sync'") from exc
    if service.journal.exists():
        raise PendingTransactionError(
            f"pending transaction exists at {service.journal.path}; reconcile it first"
        )
    endpoint = f"{stream_url.rstrip('/')}/ws/{game_id}"
    output_dir.mkdir(parents=True, exist_ok=True)
    simulated_state = None
    print(f"Watching {endpoint}; {'executing' if execute else 'planning'} move events.")
    async with connect(endpoint, max_size=262_144) as socket:
        async for raw in socket:
            try:
                message = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValidationError(
                    f"invalid JSON from Lichess stream: {exc}"
                ) from exc
            if not isinstance(message, dict):
                raise ValidationError("Lichess stream returned a non-object message")
            kind = message.get("type")
            if kind == "move":
                if execute:
                    state = service.store.load()
                    move = stream_event_to_move(
                        message,
                        service.config.board.width,
                        service.config.board.height,
                        state,
                    )
                    move_path = output_dir / f"{move.event_id}.json"
                    move_path.write_text(
                        json.dumps(move.to_dict(), indent=2, sort_keys=True) + "\n",
                        encoding="ascii",
                    )
                    plan = service.execute(move)
                    (output_dir / f"{move.event_id}.gcode").write_text(
                        plan.program.text(), encoding="ascii"
                    )
                    print(
                        f"Executed {move.event_id}; board revision {plan.next_state.revision}."
                    )
                else:
                    if simulated_state is None:
                        simulated_state = service.store.load()
                    move = stream_event_to_move(
                        message,
                        service.config.board.width,
                        service.config.board.height,
                        simulated_state,
                    )
                    plan = service.plan(move, simulated_state)
                    simulated_state = plan.next_state
                    move_path = output_dir / f"{move.event_id}.json"
                    move_path.write_text(
                        json.dumps(move.to_dict(), indent=2, sort_keys=True) + "\n",
                        encoding="ascii",
                    )
                    (output_dir / f"{move.event_id}.gcode").write_text(
                        plan.program.text(), encoding="ascii"
                    )
                    print(f"Planned {move.event_id}: {move_path}")
            elif kind in {"error", "game_over"}:
                print(json.dumps(message, sort_keys=True))
                if kind == "error" and message.get("fatal"):
                    raise ConfigurationError(
                        str(message.get("message", "fatal Lichess stream error"))
                    )
                if kind == "game_over":
                    service.finish_game()
                    return
