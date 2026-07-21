from __future__ import annotations

from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import contextlib
import json
import unittest

from chess_gantry.cli import run

ROOT = Path(__file__).resolve().parents[1]


class RunCommandTests(unittest.TestCase):
    def args(self, *command: str) -> list[str]:
        self.addCleanup(self._temporary.cleanup)
        return [
            "--config",
            str(ROOT / "config.example.json"),
            "--state",
            str(ROOT / "examples/board_state.standard.json"),
            "--journal",
            str(Path(self._temporary.name) / "pending.json"),
            "--audit",
            str(Path(self._temporary.name) / "audit.jsonl"),
            *command,
        ]

    def setUp(self) -> None:
        self._temporary = TemporaryDirectory()

    def test_run_dry_run_prints_gcode_from_example_json(self) -> None:
        buffer = StringIO()
        with contextlib.redirect_stdout(buffer):
            code = run(
                self.args(
                    "run",
                    str(ROOT / "examples/move_e2_e4.json"),
                )
            )
        self.assertEqual(code, 0)
        output = buffer.getvalue()
        self.assertIn("G21", output)
        self.assertIn("G90", output)
        self.assertIn("G0", output)

    def test_run_summary_json(self) -> None:
        buffer = StringIO()
        with contextlib.redirect_stdout(buffer):
            code = run(
                self.args(
                    "run",
                    str(ROOT / "examples/move_e2_e4.json"),
                    "--summary-json",
                )
            )
        self.assertEqual(code, 0)
        summary = json.loads(buffer.getvalue())
        self.assertEqual(summary["piece_id"], "white_pawn_e")
        self.assertEqual(summary["from"], {"x": 4, "y": 1})
        self.assertEqual(summary["to"], {"x": 4, "y": 3})

    def test_json_path_module_shortcut(self) -> None:
        buffer = StringIO()
        with contextlib.redirect_stdout(buffer):
            code = run(
                self.args(
                    str(ROOT / "examples/move_e2_e4.json"),
                )
            )
        self.assertEqual(code, 0)
        self.assertIn("G21", buffer.getvalue())

    def test_motor_test_without_confirmation_is_gcode_only(self) -> None:
        buffer = StringIO()
        with contextlib.redirect_stdout(buffer):
            code = run(self.args("motor-test"))
        self.assertEqual(code, 0)
        output = buffer.getvalue()
        self.assertIn("DRY RUN ONLY", output)
        self.assertIn("G92 X0 Y170 E0", output)
        self.assertNotIn("G28", output)
        self.assertIn("M82", output)
        self.assertIn("M302 P1", output)
        self.assertIn("M92 X80 Y80 E80", output)
        self.assertIn("M203 X20 Y20 E20", output)
        self.assertIn("M201 X200 Y200 E200", output)
        self.assertIn("M205 X3 Y3 E3", output)
        self.assertIn("G1 E5 F600", output)
        self.assertIn("G1 X5 Y165 F849", output)
        self.assertIn("G1 E0 F600", output)
        self.assertIn("G1 X0 Y170 F849", output)
        self.assertIn("M302 P0", output)


if __name__ == "__main__":
    unittest.main()
