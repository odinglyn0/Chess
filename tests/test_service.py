from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from chess_gantry.config import AppConfig
from chess_gantry.errors import ConfigurationError, SerialProtocolError
from chess_gantry.models import BoardState, GridPosition, MoveDelta
from chess_gantry.persistence import atomic_write_json, read_json
from chess_gantry.serial_link import CommandResult
from chess_gantry.service import GantryService

ROOT = Path(__file__).resolve().parents[1]


def test_config(*, calibrated: bool = True, capture: bool = True) -> AppConfig:
    raw = json.loads((ROOT / "config.example.json").read_text(encoding="utf-8"))
    raw["planner"]["kind"] = "direct"
    raw["capture"]["enabled"] = capture
    raw["safety"]["calibrated"] = calibrated
    raw["safety"]["home_before_execute"] = False
    raw["safety"]["preflight_commands"] = []
    raw["workspace"]["max_x_mm"] = 350.0
    raw["workspace"]["max_y_mm"] = 350.0
    return AppConfig.from_mapping(raw)


class FakeLink:
    def __init__(
        self, fail: bool = False, endstops=None, endstop_sequence=None
    ) -> None:
        self.fail = fail
        self.connected = True
        self.programs = []
        self.best_effort_programs = []
        self.stopped = False
        self.endstops = endstops or {
            "x_min": True,
            "y_max": True,
            "z_max": True,
        }
        self.endstop_sequence = list(endstop_sequence or [])
        self.connection_info = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return None

    def send_program(self, commands):
        commands = tuple(commands)
        self.programs.append(commands)
        if self.fail:
            raise SerialProtocolError("simulated serial failure")
        return ()

    def send_command(self, command, timeout_s=None):
        if command == "M119":
            if self.endstop_sequence:
                self.endstops = self.endstop_sequence.pop(0)
            responses = tuple(
                f"{name}: {'TRIGGERED' if triggered else 'open'}"
                for name, triggered in self.endstops.items()
            )
            return CommandResult(command, (*responses, "ok"))
        if command == "M114":
            return CommandResult(command, ("X:0.00 Y:350.00 Z:350.00 E:0.00", "ok"))
        return CommandResult(command, ("ok",))

    def best_effort(self, commands):
        self.best_effort_programs.append(tuple(commands))

    def emergency_stop(self, command):
        self.stopped = True


class ServiceTests(unittest.TestCase):
    def minimal_state(self) -> BoardState:
        return BoardState.from_mapping(
            {
                "schema_version": 1,
                "revision": 0,
                "pieces": {
                    "white_pawn_e": {"status": "board", "x": 4, "y": 1},
                },
                "processed_events": [],
            }
        )

    def capture_state(self) -> BoardState:
        return BoardState.from_mapping(
            {
                "schema_version": 1,
                "revision": 0,
                "pieces": {
                    "white_pawn_e": {"status": "board", "x": 4, "y": 3},
                    "black_pawn_d": {"status": "board", "x": 3, "y": 4},
                },
                "processed_events": [],
            }
        )

    def paths(self, temp: Path):
        return (
            temp / "board.json",
            temp / "pending.json",
            temp / "audit.jsonl",
        )

    def test_plan_does_not_change_state(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            state = self.minimal_state()
            atomic_write_json(state_path, state.to_dict())
            service = GantryService(test_config(), state_path, journal_path, audit_path)
            move = MoveDelta.from_mapping(
                {"position": "white_pawn_e", "px": 4, "py": 1, "nx": 4, "ny": 3}
            )
            plan = service.plan(move)
            self.assertEqual(plan.next_state.revision, 1)
            self.assertEqual(service.store.load().revision, 0)
            self.assertFalse(journal_path.exists())
            commands = plan.program.commands
            self.assertIn("M106 P0 S255", commands)
            self.assertIn("M107 P0", commands)
            self.assertLess(
                commands.index("M106 P0 S255"),
                commands.index("G1 X280 Y70 Z90 F3000"),
            )

    def test_reference_gantry_requires_all_three_endstops(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink(endstops={"x_min": True, "y_max": True, "z_max": False})
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            with self.assertRaisesRegex(ConfigurationError, "z_max"):
                service.reference_gantry()
            self.assertEqual(fake.programs, [])

    def test_reference_gantry_assigns_mirrored_xye_origin(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink()
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            program = service.reference_gantry()
            self.assertIn("G92 X0 Y350 Z350", program)
            self.assertEqual(fake.programs, [program])

    def test_home_gantry_runs_marlin_g28_and_saves_responses(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink()
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            record_path = temp / "gantry_home.json"
            record = service.home_gantry(record_path)
            self.assertEqual(
                fake.programs, [("M107 P0", "G21", "G28 X Y Z", "M400")]
            )
            self.assertEqual(record["method"], "marlin_g28")
            saved = read_json(record_path)
            self.assertIn("x_min: TRIGGERED", saved["endstop_response"])
            self.assertIn("X:0.00 Y:350.00 Z:350.00 E:0.00", saved["position_response"])

    def test_home_gantry_failure_does_not_save_record(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink(fail=True)
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            record_path = temp / "gantry_home.json"
            with self.assertRaises(SerialProtocolError):
                service.home_gantry(record_path)
            self.assertFalse(record_path.exists())
            self.assertEqual(
                fake.best_effort_programs[-1],
                ("M107 P0", "M84"),
            )

    def test_workspace_test_visits_grid_and_returns_to_reference(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink()
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            program = service.workspace_test(1200.0, 20.0, 8, 8, 100)
            moves = tuple(command for command in program if command.startswith("G1 "))
            self.assertEqual(len(moves), 65)
            self.assertEqual(moves[0], "G1 X330 Y20 Z20 F1200")
            self.assertEqual(moves[7], "G1 X330 Y20 Z330 F1200")
            self.assertEqual(moves[8], "G1 X285.714 Y64.286 Z330 F1200")
            self.assertEqual(moves[-1], "G1 X0 Y350 Z350 F1200")
            self.assertFalse(any(command.startswith("M106") for command in program))
            self.assertEqual(len(fake.programs), 2)

    def test_capture_generates_two_transfers_and_updates_expected_state(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.capture_state().to_dict())
            service = GantryService(test_config(), state_path, journal_path, audit_path)
            move = MoveDelta.from_mapping(
                {"position": "white_pawn_e", "px": 4, "py": 3, "nx": 3, "ny": 4}
            )
            plan = service.plan(move)
            self.assertEqual(
                [transfer.purpose for transfer in plan.transfers], ["capture", "move"]
            )
            self.assertEqual(plan.captured_piece_id, "black_pawn_d")
            self.assertEqual(plan.next_state.pieces["black_pawn_d"].capture_slot, 0)
            self.assertEqual(
                plan.next_state.pieces["white_pawn_e"].board_position,
                GridPosition(3, 4),
            )

    def test_en_passant_capture_starts_at_explicit_capture_square(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            state = BoardState.from_mapping(
                {
                    "schema_version": 1,
                    "revision": 0,
                    "pieces": {
                        "white_pawn_e": {"status": "board", "x": 4, "y": 4},
                        "black_pawn_d": {"status": "board", "x": 3, "y": 4},
                    },
                    "processed_events": [],
                }
            )
            atomic_write_json(state_path, state.to_dict())
            service = GantryService(test_config(), state_path, journal_path, audit_path)
            move = MoveDelta.from_mapping(
                {
                    "position": "white_pawn_e",
                    "px": 4,
                    "py": 4,
                    "nx": 3,
                    "ny": 5,
                    "capture": {"id": "black_pawn_d", "x": 3, "y": 4},
                }
            )
            plan = service.plan(move)
            self.assertEqual(plan.transfers[0].purpose, "capture")
            self.assertEqual(plan.transfers[0].start.x, 70.0)
            self.assertEqual(plan.transfers[0].start.y, 90.0)
            self.assertEqual(plan.transfers[1].end.x, 70.0)
            self.assertEqual(plan.transfers[1].end.y, 110.0)

    def test_successful_execute_commits_state_and_clears_journal(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink()
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            move = MoveDelta.from_mapping(
                {
                    "event_id": "event-1",
                    "position": "white_pawn_e",
                    "px": 4,
                    "py": 1,
                    "nx": 4,
                    "ny": 3,
                }
            )
            service.execute(move)
            stored = service.store.load()
            self.assertEqual(stored.revision, 1)
            self.assertEqual(
                stored.pieces["white_pawn_e"].board_position, GridPosition(4, 3)
            )
            self.assertIn("event-1", stored.processed_events)
            self.assertFalse(journal_path.exists())
            self.assertEqual(len(fake.programs), 1)

    def test_failed_execute_keeps_state_and_leaves_reconcilable_journal(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink(fail=True)
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            move = MoveDelta.from_mapping(
                {"position": "white_pawn_e", "px": 4, "py": 1, "nx": 4, "ny": 3}
            )
            with self.assertRaisesRegex(SerialProtocolError, "simulated"):
                service.execute(move)
            self.assertEqual(service.store.load().revision, 0)
            self.assertTrue(journal_path.exists())
            self.assertEqual(service.journal.load()["status"], "failed_or_unknown")
            self.assertEqual(
                fake.best_effort_programs,
                [("M107 P0", "M211 S1")],
            )

            reconciled = service.reconcile_mark_applied()
            self.assertEqual(reconciled.revision, 1)
            self.assertEqual(
                service.store.load().pieces["white_pawn_e"].board_position,
                GridPosition(4, 3),
            )
            self.assertFalse(journal_path.exists())

    def test_execute_is_locked_until_calibrated(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            service = GantryService(
                test_config(calibrated=False), state_path, journal_path, audit_path
            )
            move = MoveDelta.from_mapping(
                {"position": "white_pawn_e", "px": 4, "py": 1, "nx": 4, "ny": 3}
            )
            with self.assertRaisesRegex(ConfigurationError, "calibrated is false"):
                service.execute(move)
            self.assertFalse(journal_path.exists())

    def test_motor_test_runs_without_homing_and_does_not_change_board_state(
        self,
    ) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink()
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            program = service.motor_test()
            self.assertEqual(fake.programs, [program])
            self.assertNotIn("M82", program)
            self.assertFalse(any(command.startswith("M302") for command in program))
            self.assertIn("M92 X80 Y80 Z80", program)
            self.assertIn("M203 X200 Y200 Z50", program)
            self.assertIn("M201 X500 Y500 Z300", program)
            self.assertIn("M205 X5 Y5 Z5", program)
            self.assertIn("G92 X0 Y350 Z350", program)
            self.assertFalse(any(command.startswith("G28") for command in program))
            self.assertTrue(any(" Z" in command for command in program))
            self.assertFalse(any(" E" in command for command in program))
            self.assertIn("G1 Z330 F600", program)
            self.assertIn("G1 X20 Y330 F600", program)
            self.assertIn("G1 Z350 F600", program)
            self.assertIn("G1 X0 Y350 F600", program)
            self.assertEqual(program[-2:], ("M211 S1", "M84"))
            self.assertEqual(program[-1], "M84")
            self.assertEqual(service.store.load().revision, 0)
            self.assertFalse(journal_path.exists())

    def test_motor_test_requires_workspace_and_calibration(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            locked = GantryService(
                test_config(calibrated=False), state_path, journal_path, audit_path
            )
            with self.assertRaisesRegex(ConfigurationError, "calibrated is false"):
                locked.motor_test()

    def test_motor_test_rejects_unsafe_distance_and_feed(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            service = GantryService(test_config(), state_path, journal_path, audit_path)
            with self.assertRaisesRegex(ConfigurationError, "distance"):
                service.motor_test_program(500.0, 600.0)
            with self.assertRaisesRegex(ConfigurationError, "cannot exceed"):
                service.motor_test_program(20.0, 50000.0)
            with self.assertRaisesRegex(ConfigurationError, "more than 5 seconds"):
                service.motor_test_program(100.0, 600.0, magnet_on=True)

    def test_motor_test_pulses_fan_one_during_each_move(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink()
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            program = service.motor_test(20.0, 1200.0, magnet_on=True)
            self.assertEqual(program.count("M106 P0 S255"), 1)
            self.assertEqual(program.count("G4 P300"), 2)
            first_on = program.index("M106 P0 S255")
            self.assertEqual(
                program[first_on : first_on + 4],
                ("M106 P0 S255", "G4 P300", "G1 Z330 F1200", "M400"),
            )
            self.assertLess(
                program.index("G1 X20 Y330 F1200"), program.index("M107 P0", first_on)
            )
            self.assertEqual(program[-3:], ("M107 P0", "M211 S1", "M84"))
            self.assertEqual(fake.programs, [program])

    def test_motor_presentation_keeps_full_power_until_all_loops_finish(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            service = GantryService(test_config(), state_path, journal_path, audit_path)
            program = service.motor_test_program(
                20.0, 1200.0, magnet_on=True, presentation_loops=3
            )
            moves = [command for command in program if command.startswith("G1 ")]
            first_on = program.index("M106 P0 S255")
            first_off = program.index("M107 P0", first_on)
            self.assertEqual(len(moves), 12)
            self.assertEqual(program.count("M106 P0 S255"), 13)
            self.assertGreater(first_off, program.index(moves[-1]))
            self.assertEqual(program[first_off], "M107 P0")

    def test_motor_presentation_rejects_unbounded_power_duration(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            service = GantryService(test_config(), state_path, journal_path, audit_path)
            with self.assertRaisesRegex(ConfigurationError, "more than 30 seconds"):
                service.motor_test_program(
                    100.0, 600.0, magnet_on=True, presentation_loops=2
                )

    def test_piece_demo_requires_three_endstops_before_movement(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink(endstops={"x_min": True, "y_max": False, "z_max": True})
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            with self.assertRaisesRegex(ConfigurationError, "y_max"):
                service.piece_demo(20.0, 1200.0)
            self.assertEqual(fake.programs, [])

    def test_piece_demo_holds_magnet_outbound_then_releases_and_returns(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink()
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            program = service.piece_demo(20.0, 1200.0)
            on_index = program.index("M106 P0 S255")
            inner_out = program.index("G1 Z330 F1200")
            outer_out = program.index("G1 X20 Y330 F1200")
            release = program.index("M107 P0", on_index)
            inner_return = program.index("G1 Z350 F1200")
            outer_return = program.index("G1 X0 Y350 F1200")
            self.assertLess(on_index, inner_out)
            self.assertLess(inner_out, outer_out)
            self.assertLess(outer_out, release)
            self.assertLess(release, inner_return)
            self.assertLess(inner_return, outer_return)
            self.assertEqual(len(fake.programs), 2)
            self.assertEqual(service.store.load().revision, 0)

    def test_magnet_test_uses_configured_fan_output(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink()
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            program = service.magnet_test(1.5)
            self.assertEqual(
                program,
                (
                    "M107 P0",
                    "M400",
                    "M106 P0 S255",
                    "G4 P1500",
                    "M107 P0",
                    "M400",
                ),
            )
            self.assertEqual(fake.programs, [program])

    def test_magnet_test_rejects_long_pulse_and_attempts_shutoff(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink(fail=True)
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            with self.assertRaisesRegex(ConfigurationError, "no more than 5"):
                service.magnet_test_program(5.1)
            with self.assertRaisesRegex(ConfigurationError, "no more than 5"):
                service.magnet_test_program(float("nan"))
            with self.assertRaises(SerialProtocolError):
                service.magnet_test(1.0)
            self.assertEqual(fake.best_effort_programs, [("M107 P0",)])

    def test_board_sweep_visits_every_square_and_controls_magnet(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink()
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            program = service.board_sweep(1800.0, magnet_on=True)
            moves = tuple(
                command for command in program if command.startswith(("G0 ", "G1 "))
            )
            self.assertEqual(len(moves), 64)
            self.assertEqual(moves[0], "G0 X340 Y10 Z10 F1800")
            self.assertEqual(moves[7], "G1 X340 Y10 Z150 F1800")
            self.assertEqual(moves[8], "G1 X320 Y30 Z150 F1800")
            self.assertEqual(moves[15], "G1 X320 Y30 Z10 F1800")
            self.assertEqual(moves[-1], "G1 X200 Y150 Z10 F1800")
            on_index = program.index("M106 P0 S255")
            final_off = len(program) - 1 - program[::-1].index("M107 P0")
            self.assertEqual(program.count("M106 P0 S255"), 64)
            self.assertLess(on_index, program.index(moves[1]))
            self.assertGreater(final_off, program.index(moves[-1]))
            self.assertEqual(program[-2:], ("M211 S1", "M84"))
            self.assertEqual(fake.programs, [program])

    def test_board_sweep_rejects_excess_speed_and_shuts_down_on_failure(self) -> None:
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            state_path, journal_path, audit_path = self.paths(temp)
            atomic_write_json(state_path, self.minimal_state().to_dict())
            fake = FakeLink(fail=True)
            service = GantryService(
                test_config(),
                state_path,
                journal_path,
                audit_path,
                link_factory=lambda settings: fake,
            )
            with self.assertRaisesRegex(ConfigurationError, "cannot exceed"):
                service.board_sweep_program(50000.0)
            with self.assertRaises(SerialProtocolError):
                service.board_sweep(1800.0, magnet_on=True)
            self.assertEqual(
                fake.best_effort_programs,
                [("M107 P0", "M211 S1", "M84")],
            )


if __name__ == "__main__":
    unittest.main()
