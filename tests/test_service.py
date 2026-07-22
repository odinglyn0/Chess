from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from chess_gantry.config import AppConfig
from chess_gantry.errors import ConfigurationError, SerialProtocolError
from chess_gantry.models import BoardState, GridPosition, MoveDelta
from chess_gantry.persistence import atomic_write_json
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
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.connected = True
        self.programs = []
        self.best_effort_programs = []
        self.stopped = False

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
            self.assertIn("M106 S255", commands)
            self.assertIn("M107", commands)
            self.assertLess(
                commands.index("M106 S255"), commands.index("G1 X70 Y280 E90 F3000")
            )

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
                fake.best_effort_programs, [("M107", "M302 P0", "M211 S1")]
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
            self.assertIn("M82", program)
            self.assertIn("M302 P1", program)
            self.assertIn("M92 X80 Y80 E80", program)
            self.assertIn("M203 X200 Y200 E50", program)
            self.assertIn("M201 X500 Y500 E300", program)
            self.assertIn("M205 X5 Y5 E5", program)
            self.assertIn("G92 X0 Y350 E0", program)
            self.assertFalse(any(command.startswith("G28") for command in program))
            self.assertFalse(any(" Z" in command for command in program))
            self.assertIn("G1 E200 F3000", program)
            self.assertIn("G1 X200 Y150 F16971", program)
            self.assertIn("G1 E0 F3000", program)
            self.assertIn("G1 X0 Y350 F16971", program)
            self.assertEqual(program[-3:], ("M302 P0", "M211 S1", "M84"))
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


if __name__ == "__main__":
    unittest.main()
