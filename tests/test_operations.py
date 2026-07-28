from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import time
import unittest

from chess_gantry.errors import ConfigurationError, ValidationError
from chess_gantry.operations import Confirmation, OperationManager, OperationSpec


class FakeController:
    connected = False

    def disconnect(self):
        self.connected = False


class OperationManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.quick = OperationSpec(
            "quick",
            "Quick check",
            "Print one line.",
            "Checks",
            (sys.executable, "-c", "print('operation passed')"),
        )
        self.slow = OperationSpec(
            "slow",
            "Slow check",
            "Wait until cancelled.",
            "Checks",
            (
                sys.executable,
                "-c",
                "import time; print('started', flush=True); time.sleep(30)",
            ),
            long_running=True,
        )
        self.physical = OperationSpec(
            "physical",
            "Physical check",
            "Requires confirmation.",
            "Hardware",
            (sys.executable, "-c", "print('physical')"),
            physical=True,
            confirmations=(Confirmation("clear", "Workspace is clear."),),
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def wait_for_terminal(self, manager: OperationManager) -> dict:
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            status = manager.status()
            if status["run"]["state"] not in {"starting", "running", "stopping"}:
                return status
            time.sleep(0.02)
        self.fail("operation did not finish")

    def test_runs_allowlisted_command_and_captures_logs(self) -> None:
        manager = OperationManager(self.root, FakeController(), (self.quick,))
        manager.start("quick")
        result = self.wait_for_terminal(manager)
        self.assertEqual(result["run"]["state"], "completed")
        self.assertEqual(result["run"]["returncode"], 0)
        self.assertIn("operation passed", result["logs"])

    def test_rejects_unknown_operation_and_missing_confirmation(self) -> None:
        manager = OperationManager(self.root, FakeController(), (self.physical,))
        with self.assertRaisesRegex(ValidationError, "unknown"):
            manager.start("missing")
        with self.assertRaisesRegex(ValidationError, "Workspace is clear"):
            manager.start("physical")

    def test_demo_mode_blocks_physical_operation(self) -> None:
        manager = OperationManager(
            self.root, FakeController(), (self.physical,), allow_physical=False
        )
        self.assertFalse(manager.catalog()[0]["enabled"])
        with self.assertRaisesRegex(ConfigurationError, "disabled"):
            manager.start("physical", {"clear": True})

    def test_prevents_overlap_and_cancels_process_group(self) -> None:
        manager = OperationManager(self.root, FakeController(), (self.slow, self.quick))
        manager.start("slow")
        deadline = time.monotonic() + 3
        while "started" not in manager.status()["logs"] and time.monotonic() < deadline:
            time.sleep(0.02)
        with self.assertRaisesRegex(ConfigurationError, "already running"):
            manager.start("quick")
        stopped = manager.stop()
        self.assertEqual(stopped["run"]["state"], "cancelled")
        time.sleep(0.05)
        self.assertEqual(manager.status()["run"]["state"], "cancelled")


if __name__ == "__main__":
    unittest.main()
