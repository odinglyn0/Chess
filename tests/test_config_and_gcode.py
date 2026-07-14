from __future__ import annotations

from pathlib import Path
import json
import unittest

from chess_gantry.config import AppConfig
from chess_gantry.errors import ConfigurationError
from chess_gantry.gcode import GCodeGenerator
from chess_gantry.models import MachinePoint, PieceTransfer

ROOT = Path(__file__).resolve().parents[1]


class ConfigAndGCodeTests(unittest.TestCase):
    def raw_config(self):
        return json.loads((ROOT / "config.example.json").read_text(encoding="utf-8"))

    def test_example_config_is_hardware_locked(self) -> None:
        config = AppConfig.from_mapping(self.raw_config())
        self.assertFalse(config.safety.calibrated)
        self.assertTrue(config.safety.home_before_execute)

    def test_rejects_capture_slot_outside_workspace(self) -> None:
        raw = self.raw_config()
        raw["capture"]["slots"][0] = [999.0, 999.0]
        with self.assertRaisesRegex(ConfigurationError, "outside the workspace"):
            AppConfig.from_mapping(raw)


    def test_rejects_capture_slot_inside_board(self) -> None:
        raw = self.raw_config()
        raw["capture"]["slots"][0] = [10.0, 10.0]
        with self.assertRaisesRegex(ConfigurationError, "playing-board footprint"):
            AppConfig.from_mapping(raw)

    def test_rejects_duplicate_capture_slot(self) -> None:
        raw = self.raw_config()
        raw["capture"]["slots"][1] = list(raw["capture"]["slots"][0])
        with self.assertRaisesRegex(ConfigurationError, "duplicates"):
            AppConfig.from_mapping(raw)

    def test_gcode_waits_before_magnet_transitions(self) -> None:
        raw = self.raw_config()
        raw["motion"]["park_after_move"] = False
        raw["motion"].pop("park_x_mm")
        raw["motion"].pop("park_y_mm")
        config = AppConfig.from_mapping(raw)
        transfer = PieceTransfer(
            piece_id="piece-1",
            purpose="move",
            start=MachinePoint(10.0, 10.0),
            end=MachinePoint(30.0, 30.0),
            path=(MachinePoint(10.0, 10.0), MachinePoint(20.0, 15.0), MachinePoint(30.0, 30.0)),
        )
        commands = GCodeGenerator(config).generate([transfer]).commands
        on_index = commands.index("M106 S255")
        first_drag = commands.index("G1 X20 Y15 F600")
        final_drag = commands.index("G1 X30 Y30 F600")
        off_after_drag = next(index for index in range(final_drag + 1, len(commands)) if commands[index] == "M107")
        self.assertEqual(commands[on_index - 1], "M400")
        self.assertLess(on_index, first_drag)
        self.assertEqual(commands[off_after_drag - 1], "M400")


if __name__ == "__main__":
    unittest.main()
