from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from chess_gantry.config import AppConfig
from chess_gantry.controller import GantryController
from chess_gantry.errors import ConfigurationError, ValidationError
from chess_gantry.models import BoardState, GridPosition
from chess_gantry.persistence import atomic_write_json
from chess_gantry.service import GantryService

ROOT = Path(__file__).resolve().parents[1]


def controller_config(
    *, calibrated: bool = True, home_before_execute: bool = True
) -> AppConfig:
    raw = json.loads((ROOT / "config.example.json").read_text(encoding="utf-8"))
    raw["planner"]["kind"] = "direct"
    raw["capture"]["enabled"] = False
    raw["capture"]["slots"] = []
    raw["safety"]["calibrated"] = calibrated
    raw["safety"]["home_before_execute"] = home_before_execute
    raw["safety"]["preflight_commands"] = []
    return AppConfig.from_mapping(raw)


def minimal_state() -> BoardState:
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


class ControllerTests(unittest.TestCase):
    def make_controller(self, directory: str, **config_kwargs):
        root = Path(directory)
        config = controller_config(**config_kwargs)
        state_path = root / "state.json"
        atomic_write_json(state_path, minimal_state().to_dict())
        service = GantryService(
            config,
            state_path,
            root / "pending.json",
            root / "audit.jsonl",
        )
        return GantryController(config, service, demo=True), service

    def test_manual_coordinate_workflow_uses_shared_connection(self) -> None:
        with TemporaryDirectory() as directory:
            controller, _ = self.make_controller(directory)
            status = controller.connect()
            self.assertTrue(status["connected"])
            self.assertEqual(status["port"], "DEMO")

            with self.assertRaisesRegex(ConfigurationError, "outer X/Y"):
                controller.move_to_mm(x_mm=10, y_mm=10, feed_mm_min=600)

            controller.home_xy()
            status = controller.move_to_mm(x_mm=25.5, y_mm=30.25, feed_mm_min=600)
            self.assertEqual(status["position_mm"], {"x": 25.5, "y": 30.25})
            self.assertIn("G1 X269.750 Y30.250 Z25.500 F600", controller._link.commands)
            self.assertFalse(
                any(command.startswith("M302") for command in controller._link.commands)
            )

    def test_jog_updates_logical_and_raw_machine_coordinates(self) -> None:
        with TemporaryDirectory() as directory:
            controller, _ = self.make_controller(directory)
            controller.connect()
            with self.assertRaisesRegex(ConfigurationError, "home"):
                controller.jog(delta_x_mm=1, delta_y_mm=0, feed_mm_min=600)
            controller.home_xy()
            controller.jog(delta_x_mm=-5, delta_y_mm=0, feed_mm_min=600)
            status = controller.jog(delta_x_mm=0, delta_y_mm=-10, feed_mm_min=600)
            self.assertEqual(status["position_mm"], {"x": 323.0, "y": 288.0})
            self.assertEqual(
                status["machine_position_mm"],
                {"x": 12.0, "y": 288.0, "z": 323.0},
            )

    def test_jog_rejects_diagonal_oversized_and_out_of_bounds_moves(self) -> None:
        with TemporaryDirectory() as directory:
            controller, _ = self.make_controller(directory)
            controller.connect()
            controller.home_xy()
            with self.assertRaisesRegex(ValidationError, "exactly one"):
                controller.jog(delta_x_mm=1, delta_y_mm=1, feed_mm_min=600)
            with self.assertRaisesRegex(ValidationError, "20 mm"):
                controller.jog(delta_x_mm=-21, delta_y_mm=0, feed_mm_min=600)
            with self.assertRaisesRegex(ValidationError, "outside"):
                controller.jog(delta_x_mm=3, delta_y_mm=0, feed_mm_min=600)

    def test_plan_is_read_only_and_execute_commits_through_same_link(self) -> None:
        with TemporaryDirectory() as directory:
            controller, service = self.make_controller(directory)
            move = {
                "event_id": "controller-1",
                "position": "white_pawn_e",
                "px": 4,
                "py": 1,
                "nx": 4,
                "ny": 3,
            }
            plan = controller.plan_move(move)
            self.assertEqual(plan.next_state.revision, 1)
            self.assertEqual(service.store.load().revision, 0)

            controller.connect()
            with self.assertRaisesRegex(ConfigurationError, "motion confirmation"):
                controller.execute_move(move, confirm_motion=False)

            completed = controller.execute_move(move, confirm_motion=True)
            self.assertEqual(completed.next_state.revision, 1)
            stored = service.store.load()
            self.assertEqual(
                stored.pieces["white_pawn_e"].board_position, GridPosition(4, 3)
            )
            self.assertFalse(service.journal.exists())

    def test_execution_remains_locked_by_config(self) -> None:
        with TemporaryDirectory() as directory:
            controller, _ = self.make_controller(directory, calibrated=False)
            controller.connect()
            move = {"position": "white_pawn_e", "px": 4, "py": 1, "nx": 4, "ny": 3}
            with self.assertRaisesRegex(ConfigurationError, "calibrated is false"):
                controller.execute_move(move, confirm_motion=True)


if __name__ == "__main__":
    unittest.main()
