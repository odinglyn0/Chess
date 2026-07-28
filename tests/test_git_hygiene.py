from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GitHygieneTests(unittest.TestCase):
    def test_repository_has_no_tracked_dependencies_or_runtime_data(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_git_hygiene.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
