from __future__ import annotations

from argparse import ArgumentParser, Namespace
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence
import json
import sys
import asyncio

from .config import AppConfig
from .errors import GantryError, PendingTransactionError, ValidationError
from .models import BoardState, MoveDelta
from .persistence import read_json
from .serial_link import MarlinSerial, discover_serial_ports
from .service import GantryService
from .lichess_adapter import stream_event_to_move
from .lichess_watch import watch_game
from .lichess_pgn import fetch_pgn, pgn_moves
from .lichess_follow import follow_game
from .uci_adapter import uci_to_move


def _parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="chess-gantry", description="Plan and stream chess-gantry G-code to Marlin"
    )
    parser.add_argument(
        "--config", default="config.json", help="gantry configuration JSON"
    )
    parser.add_argument(
        "--state", default="data/board_state.json", help="persistent board-state JSON"
    )
    parser.add_argument(
        "--journal",
        default="data/pending_move.json",
        help="pending transaction journal",
    )
    parser.add_argument(
        "--audit", default="data/audit.jsonl", help="append-only audit log"
    )

    commands = parser.add_subparsers(dest="command", required=True)

    plan = commands.add_parser(
        "plan", help="validate a move and print/write G-code without moving hardware"
    )
    plan.add_argument("move_json", help="move-delta JSON file")
    plan.add_argument("--output", "-o", help="write G-code to this file")
    plan.add_argument(
        "--summary-json",
        action="store_true",
        help="print plan summary as JSON before G-code",
    )

    validate = commands.add_parser(
        "validate",
        help="validate move, board state, and path without outputting G-code",
    )
    validate.add_argument("move_json", help="move-delta JSON file")

    execute = commands.add_parser(
        "execute", help="send a move over serial and commit board state on success"
    )
    execute.add_argument("move_json", help="move-delta JSON file")
    execute.add_argument(
        "--confirm-motion",
        action="store_true",
        help="required acknowledgement that the physical workspace is clear",
    )

    run = commands.add_parser(
        "run",
        help="read move JSON, generate G-code, and stream it to Marlin (dry-run without --confirm-motion)",
    )
    run.add_argument(
        "move_json", help="move-delta JSON file (e.g. examples/move_e2_e4.json)"
    )
    run.add_argument(
        "--confirm-motion",
        action="store_true",
        help="stream G-code over serial to the gantry controller and commit board state on success",
    )
    run.add_argument("--output", "-o", help="write G-code to this file")
    run.add_argument(
        "--summary-json", action="store_true", help="print plan summary as JSON"
    )

    init_state = commands.add_parser(
        "init-state", help="validate and install an initial board-state JSON"
    )
    init_state.add_argument("source_json", help="source board-state JSON")
    init_state.add_argument(
        "--overwrite", action="store_true", help="replace an existing state file"
    )

    commands.add_parser("show-state", help="print the current board state")
    uci = commands.add_parser(
        "uci-to-json",
        help="convert a legal UCI move such as e2e4 to gantry move-delta JSON",
    )
    uci.add_argument("uci_move", help="four-character UCI move, e.g. e2e4")
    uci.add_argument("--event-id", help="optional unique game/ply identifier")
    uci.add_argument(
        "--en-passant",
        action="store_true",
        help="treat a diagonal pawn move to an empty square as en passant",
    )
    uci.add_argument(
        "--output", "-o", help="write move JSON to this file instead of stdout"
    )
    lichess = commands.add_parser(
        "lichess-event",
        help="convert a move envelope from services/lichess_stream into gantry JSON and G-code",
    )
    lichess.add_argument(
        "event_json", help="saved type=move WebSocket envelope from the Lichess stream"
    )
    lichess.add_argument(
        "--move-output", help="write converted gantry move JSON to this file"
    )
    lichess.add_argument("--gcode-output", help="write planned G-code to this file")
    watch = commands.add_parser(
        "lichess-watch",
        help="subscribe to the upstream Lichess API and plan or execute moves",
    )
    watch.add_argument("game_id", help="Lichess game id")
    watch.add_argument(
        "--stream-url",
        default="ws://127.0.0.1:8010",
        help="upstream stream service URL",
    )
    watch.add_argument(
        "--output-dir",
        default="data/lichess",
        help="directory for generated event JSON and G-code",
    )
    watch.add_argument(
        "--execute",
        action="store_true",
        help="execute every received move instead of planning only",
    )
    watch.add_argument(
        "--confirm-motion", action="store_true", help="required with --execute"
    )
    pgn = commands.add_parser(
        "lichess-pgn",
        help="fetch a Lichess game and dry-run all recorded moves to JSON and G-code",
    )
    pgn.add_argument("game_id", help="Lichess game id")
    pgn.add_argument(
        "--output-dir",
        default="data/lichess",
        help="directory for generated event JSON and G-code",
    )
    follow = commands.add_parser(
        "lichess-follow",
        help="poll Lichess PGN and automatically create JSON/G-code for new moves",
    )
    follow.add_argument("game_id", help="Lichess game id")
    follow.add_argument(
        "--output-dir",
        default="data/lichess",
        help="directory for generated move JSON and G-code",
    )
    follow.add_argument("--session", help="persistent follow-session JSON path")
    follow.add_argument(
        "--interval", type=float, default=5.0, help="PGN polling interval in seconds"
    )
    follow.add_argument(
        "--once",
        action="store_true",
        help="poll once, generate available new moves, then exit",
    )
    follow.add_argument(
        "--reset-session",
        action="store_true",
        help="forget emitted move history and recreate files",
    )
    follow.add_argument(
        "--execute",
        action="store_true",
        help="stream new moves to Marlin and commit board state",
    )
    follow.add_argument(
        "--execute-existing",
        action="store_true",
        help="with --execute, also stream already dry-run recorded moves",
    )
    follow.add_argument(
        "--confirm-motion", action="store_true", help="required with --execute"
    )
    follow.add_argument(
        "--obstacle-keepout-mm",
        type=float,
        help="dry-run-only A* clearance override; does not modify config.json",
    )
    commands.add_parser("ports", help="list ranked serial ports visible to pyserial")

    diagnose = commands.add_parser(
        "diagnose",
        help="connect, verify Marlin with M115, and read endstops/position without moving",
    )
    diagnose.add_argument(
        "--port", help="override serial port; omit to use config/auto-detection"
    )
    diagnose.add_argument("--baudrate", type=int, help="try only this baud rate")

    web = commands.add_parser("web", help="launch the local browser controller")
    web.add_argument(
        "--host", default="127.0.0.1", help="bind address (default: local only)"
    )
    web.add_argument(
        "--web-port", type=int, default=8000, help="browser port (default: 8000)"
    )
    web.add_argument(
        "--no-browser", action="store_true", help="do not open a browser automatically"
    )
    web.add_argument(
        "--demo", action="store_true", help="run with a simulated Marlin controller"
    )
    web.add_argument(
        "--allow-network",
        action="store_true",
        help="allow a non-loopback bind; local-only is safer and is the default",
    )

    home = commands.add_parser(
        "home",
        help="initialize coupled outer X/Y and independent inner E coordinates without homing",
    )
    home.add_argument(
        "--confirm-motion", action="store_true", help="required before physical motion"
    )

    motor_test = commands.add_parser(
        "motor-test",
        help="print outer X/Y plus inner E sample G-code; add --confirm-motion to send it to Marlin",
    )
    motor_test.add_argument(
        "--confirm-motion",
        action="store_true",
        help="home and send the displayed test program to physical hardware",
    )
    motor_test.add_argument(
        "--demo",
        action="store_true",
        help="simulate Marlin instead of opening the serial port",
    )

    commands.add_parser(
        "stop", help="send the configured Marlin emergency-stop command immediately"
    )

    reconcile = commands.add_parser(
        "reconcile",
        help="resolve a pending move after physically checking where the pieces ended up",
    )
    action = reconcile.add_mutually_exclusive_group()
    action.add_argument(
        "--mark-applied",
        action="store_true",
        help="commit the journal's expected next state",
    )
    action.add_argument(
        "--discard",
        action="store_true",
        help="keep current state and remove the journal",
    )
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


_COMMANDS = frozenset(
    {
        "plan",
        "validate",
        "execute",
        "run",
        "init-state",
        "show-state",
        "uci-to-json",
        "lichess-event",
        "lichess-watch",
        "lichess-pgn",
        "lichess-follow",
        "ports",
        "diagnose",
        "web",
        "home",
        "motor-test",
        "stop",
        "reconcile",
    }
)


_OPTION_VALUE_FLAGS = frozenset(
    {
        "--config",
        "--state",
        "--journal",
        "--audit",
        "--port",
        "--output",
        "-o",
        "--baudrate",
    }
)


def _normalize_argv(argv: Optional[Sequence[str]]) -> Optional[Sequence[str]]:
    if argv is None:
        return None
    normalized = list(argv)
    if any(token in _COMMANDS for token in normalized):
        return normalized
    skip_next = False
    for index, token in enumerate(normalized):
        if skip_next:
            skip_next = False
            continue
        if token in _OPTION_VALUE_FLAGS:
            skip_next = True
            continue
        if token.endswith(".json") and not token.startswith("-"):
            return [*normalized[:index], "run", *normalized[index:]]
    return normalized


def run(argv: Optional[Sequence[str]] = None) -> int:
    parser = _parser()
    args = parser.parse_args(_normalize_argv(argv))

    try:
        if args.command == "ports":
            ports = discover_serial_ports()
            if not ports:
                print("No serial ports found.")
            for item in ports:
                marker = "likely-printer" if item.likely_printer else "serial"
                print(f"{item.device}\t{marker}\t{item.description}\t{item.hwid}")
            return 0

        config = AppConfig.load(args.config)

        if args.command == "diagnose":
            settings = config.serial
            if args.port:
                settings = replace(settings, port=args.port)
            if args.baudrate is not None:
                if args.baudrate <= 0:
                    parser.error("--baudrate must be positive")
                settings = replace(
                    settings,
                    baudrate=args.baudrate,
                    fallback_baudrates=(),
                )
            with MarlinSerial(settings) as link:
                info = link.connection_info
                assert info is not None
                _print_json({"connection": info.as_dict()})
                for command in ("M119", "M114"):
                    result = link.send_command(command, timeout_s=10.0)
                    print(f"\n> {command}")
                    for line in result.responses:
                        print(line)
            return 0

        if args.command == "web":
            from .web_app import run_web_server

            run_web_server(
                config=config,
                state_path=args.state,
                journal_path=args.journal,
                audit_path=args.audit,
                host=args.host,
                port=args.web_port,
                open_browser=not args.no_browser,
                demo=args.demo,
                allow_network=args.allow_network,
            )
            return 0

        if args.command == "lichess-follow" and args.obstacle_keepout_mm is not None:
            if args.execute:
                parser.error(
                    "--obstacle-keepout-mm is dry-run-only and cannot be combined with --execute"
                )
            if args.obstacle_keepout_mm <= 0:
                parser.error("--obstacle-keepout-mm must be positive")
            config = replace(
                config,
                planner=replace(
                    config.planner, obstacle_keepout_mm=args.obstacle_keepout_mm
                ),
            )
            print(
                f"Dry-run planner override: obstacle_keepout_mm={args.obstacle_keepout_mm:g}; "
                "config.json was not changed."
            )

        service = _service(args, config)

        if args.command == "init-state":
            source = BoardState.from_mapping(
                read_json(Path(args.source_json)),
                config.board.width,
                config.board.height,
            )
            service.store.initialize(source, overwrite=args.overwrite)
            print(
                f"Installed board state at {service.store.path} (revision {source.revision})."
            )
            return 0

        if args.command == "show-state":
            _print_json(service.store.load().to_dict())
            return 0

        if args.command == "uci-to-json":
            move = uci_to_move(
                args.uci_move,
                service.store.load(),
                event_id=args.event_id,
                en_passant=args.en_passant,
                width=config.board.width,
                height=config.board.height,
            )
            payload = move.to_dict()
            if args.output:
                output = Path(args.output)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(
                    json.dumps(payload, indent=2, sort_keys=True) + "\n",
                    encoding="ascii",
                )
                print(f"Wrote move JSON to {output}.")
            else:
                _print_json(payload)
            return 0

        if args.command == "lichess-event":
            if service.journal.exists():
                raise PendingTransactionError(
                    f"a pending transaction exists at {service.journal.path}; state may not match the physical board"
                )
            with service.store.locked():
                state = service.store.load()
                move = stream_event_to_move(
                    read_json(Path(args.event_json)),
                    config.board.width,
                    config.board.height,
                    state,
                )
                plan = service.plan(move, state)
            if args.move_output:
                output = Path(args.move_output)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(
                    json.dumps(move.to_dict(), indent=2, sort_keys=True) + "\n",
                    encoding="ascii",
                )
                print(f"Wrote move JSON to {output}.")
            if args.gcode_output:
                output = Path(args.gcode_output)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(plan.program.text(), encoding="ascii")
                print(f"Wrote {len(plan.program.commands)} commands to {output}.")
            _print_json(plan.summary())
            return 0

        if args.command == "lichess-watch":
            if args.execute and not args.confirm_motion:
                parser.error("lichess-watch --execute requires --confirm-motion")
            asyncio.run(
                watch_game(
                    service,
                    args.stream_url,
                    args.game_id,
                    Path(args.output_dir),
                    execute=args.execute,
                )
            )
            return 0

        if args.command == "lichess-pgn":
            if service.journal.exists():
                raise PendingTransactionError(
                    f"pending transaction exists at {service.journal.path}; reconcile it first"
                )
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            pgn = fetch_pgn(args.game_id)
            state = service.store.load()
            count = 0
            for move in pgn_moves(args.game_id, pgn, state):
                plan = service.plan(move, state)
                state = plan.next_state
                (output_dir / f"{move.event_id}.json").write_text(
                    json.dumps(move.to_dict(), indent=2, sort_keys=True) + "\n",
                    encoding="ascii",
                )
                (output_dir / f"{move.event_id}.gcode").write_text(
                    plan.program.text(), encoding="ascii"
                )
                count += 1
            print(f"Dry-run planned {count} Lichess move(s) in {output_dir}.")
            return 0

        if args.command == "lichess-follow":
            if args.execute and not args.confirm_motion:
                parser.error("lichess-follow --execute requires --confirm-motion")
            if args.execute_existing and not args.execute:
                parser.error("lichess-follow --execute-existing requires --execute")
            output_dir = Path(args.output_dir)
            session_path = (
                Path(args.session)
                if args.session
                else output_dir / f"{args.game_id}.session.json"
            )
            follow_game(
                service,
                args.game_id,
                output_dir,
                session_path,
                interval_s=args.interval,
                execute=args.execute,
                execute_existing=args.execute_existing,
                reset_session=args.reset_session,
                once=args.once,
            )
            return 0

        if args.command == "reconcile":
            if not service.journal.exists():
                raise PendingTransactionError("there is no pending transaction")
            if not args.mark_applied and not args.discard:
                _print_json(dict(service.journal.load()))
                return 0
            if not args.confirm_physical_state:
                parser.error(
                    "reconcile changes require --confirm-physical-state after inspecting the board"
                )
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

        if args.command == "motor-test":
            program = service.motor_test_program()
            if not args.confirm_motion:
                print("; DRY RUN ONLY: no serial port was opened")
                print("; outer X and Y are coupled; inner E moves independently")
                print("\n".join(program))
                return 0
            if args.demo:
                from .serial_link import DemoMarlinSerial

                link = DemoMarlinSerial(config.serial)
                with link:
                    link.send_program(config.safety.preflight_commands)
                    link.send_program(program)
                print("; DEMO ONLY: no serial port was opened")
            else:
                program = service.motor_test()
            print("; fixed outer X/Y and inner E motor test sent successfully")
            print("\n".join(program))
            return 0

        if args.command == "stop":
            service.emergency_stop()
            print(
                "Emergency-stop command sent. Marlin normally requires a reset before further operation."
            )
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

        if args.command == "run":
            if service.journal.exists():
                raise PendingTransactionError(
                    f"a pending transaction exists at {service.journal.path}; state may not match the physical board"
                )
            if not args.confirm_motion:
                with service.store.locked():
                    plan = service.plan(move, service.store.load())
                if args.summary_json:
                    _print_json(plan.summary())
                    return 0
                if args.output:
                    output = Path(args.output)
                    output.parent.mkdir(parents=True, exist_ok=True)
                    output.write_text(plan.program.text(), encoding="ascii")
                    print(
                        f"Wrote {len(plan.program.commands)} commands to {output}.",
                        file=sys.stderr,
                    )
                else:
                    print(plan.program.text(), end="")
                return 0
            plan = service.execute(move)
            if args.output:
                output = Path(args.output)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(plan.program.text(), encoding="ascii")
                print(
                    f"Wrote {len(plan.program.commands)} commands to {output}.",
                    file=sys.stderr,
                )
            if args.summary_json:
                _print_json(plan.summary())
            else:
                print(
                    f"Move completed: {plan.move.piece_id} "
                    f"({plan.move.previous.x},{plan.move.previous.y}) -> "
                    f"({plan.move.new.x},{plan.move.new.y}); "
                    f"board revision {plan.next_state.revision}.",
                    file=sys.stderr,
                )
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
