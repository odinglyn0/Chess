"""Command-line interface for dry-running and executing gantry moves."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence
import json
import sys

from .config import AppConfig
from .errors import GantryError, PendingTransactionError, ValidationError
from .models import BoardState, MoveDelta
from .persistence import read_json
from .serial_link import list_serial_ports
from .service import GantryService


def _parser() -> ArgumentParser:
    parser = ArgumentParser(prog="chess-gantry", description="Plan and stream chess-gantry G-code to Marlin")
    parser.add_argument("--config", default="config.json", help="gantry configuration JSON")
    parser.add_argument("--state", default="data/board_state.json", help="persistent board-state JSON")
    parser.add_argument("--journal", default="data/pending_move.json", help="pending transaction journal")
    parser.add_argument("--audit", default="data/audit.jsonl", help="append-only audit log")

    commands = parser.add_subparsers(dest="command", required=True)

    plan = commands.add_parser("plan", help="validate a move and print/write G-code without moving hardware")
    plan.add_argument("move_json", help="move-delta JSON file")
    plan.add_argument("--output", "-o", help="write G-code to this file")
    plan.add_argument("--summary-json", action="store_true", help="print plan summary as JSON before G-code")

    validate = commands.add_parser("validate", help="validate move, board state, and path without outputting G-code")
    validate.add_argument("move_json", help="move-delta JSON file")

    execute = commands.add_parser("execute", help="send a move over serial and commit board state on success")
    execute.add_argument("move_json", help="move-delta JSON file")
    execute.add_argument(
        "--confirm-motion",
        action="store_true",
        help="required acknowledgement that the physical workspace is clear",
    )

    init_state = commands.add_parser("init-state", help="validate and install an initial board-state JSON")
    init_state.add_argument("source_json", help="source board-state JSON")
    init_state.add_argument("--overwrite", action="store_true", help="replace an existing state file")

    commands.add_parser("show-state", help="print the current board state")
    commands.add_parser("ports", help="list serial ports visible to pyserial")

    home = commands.add_parser("home", help="turn magnet off and home X/Y using configured commands")
    home.add_argument("--confirm-motion", action="store_true", help="required before physical motion")

    commands.add_parser("stop", help="send the configured Marlin emergency-stop command immediately")

    reconcile = commands.add_parser(
        "reconcile",
        help="resolve a pending move after physically checking where the pieces ended up",
    )
    action = reconcile.add_mutually_exclusive_group()
    action.add_argument("--mark-applied", action="store_true", help="commit the journal's expected next state")
    action.add_argument("--discard", action="store_true", help="keep current state and remove the journal")
    reconcile.add_argument(
        "--confirm-physical-state",
        action="store_true",
        help="required for --mark-applied or --discard",
    )
    return parser


def _load_move(path: Path, config: AppConfig) -> MoveDelta:
    raw = read_json(path)
    return MoveDelta.from_mapping(raw, config.board.width, config.board.height)


def _service(args: Namespace, config: AppConfig) -> GantryService:
    return GantryService(config, args.state, args.journal, args.audit)


def _print_json(value: Mapping[str, Any]) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def run(argv: Optional[Sequence[str]] = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "ports":
            ports = list_serial_ports()
            if not ports:
                print("No serial ports found.")
            for device, description in ports:
                print(f"{device}\t{description}")
            return 0

        config = AppConfig.load(args.config)
        service = _service(args, config)

        if args.command == "init-state":
            source = BoardState.from_mapping(
                read_json(Path(args.source_json)),
                config.board.width,
                config.board.height,
            )
            service.store.initialize(source, overwrite=args.overwrite)
            print(f"Installed board state at {service.store.path} (revision {source.revision}).")
            return 0

        if args.command == "show-state":
            _print_json(service.store.load().to_dict())
            return 0

        if args.command == "reconcile":
            if not service.journal.exists():
                raise PendingTransactionError("there is no pending transaction")
            if not args.mark_applied and not args.discard:
                _print_json(dict(service.journal.load()))
                return 0
            if not args.confirm_physical_state:
                parser.error("reconcile changes require --confirm-physical-state after inspecting the board")
            if args.mark_applied:
                state = service.reconcile_mark_applied()
                print(f"Journal applied; board state is now revision {state.revision}.")
            else:
                service.reconcile_discard()
                print("Journal discarded; stored board state was not changed.")
            return 0

        if args.command == "home":
            if not args.confirm_motion:
                parser.error("home requires --confirm-motion")
            service.home()
            print("Homing commands completed.")
            return 0

        if args.command == "stop":
            service.emergency_stop()
            print("Emergency-stop command sent. Marlin normally requires a reset before further operation.")
            return 0

        move = _load_move(Path(args.move_json), config)

        if args.command in {"plan", "validate"}:
            if service.journal.exists():
                raise PendingTransactionError(
                    f"a pending transaction exists at {service.journal.path}; state may not match the physical board"
                )
            with service.store.locked():
                plan = service.plan(move, service.store.load())
            if args.command == "validate":
                _print_json(plan.summary())
                return 0
            if args.summary_json:
                _print_json(plan.summary())
            if args.output:
                output = Path(args.output)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(plan.program.text(), encoding="ascii")
                print(f"Wrote {len(plan.program.commands)} commands to {output}.")
            else:
                print(plan.program.text(), end="")
            return 0

        if args.command == "execute":
            if not args.confirm_motion:
                parser.error("execute requires --confirm-motion")
            plan = service.execute(move)
            _print_json(plan.summary())
            return 0

        parser.error(f"unsupported command {args.command}")
        return 2
    except GantryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130


def main() -> None:
    raise SystemExit(run())
