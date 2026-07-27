from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FirmwareScriptTests(unittest.TestCase):
    def test_check_firmware_script_imports_and_prints_help(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_firmware.py"), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validate Relay Chess Marlin firmware", result.stdout)

    def test_check_firmware_reports_connection_failure_without_traceback(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "check_firmware.py"),
                "--config",
                str(ROOT / "tests" / "missing-config.json"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Firmware check failed:", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
