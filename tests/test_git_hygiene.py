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

    def test_container_without_git_metadata_is_supported(self) -> None:
        source = (ROOT / "scripts" / "check_git_hygiene.py").read_text(encoding="utf-8")
        self.assertIn('if not (ROOT / ".git").exists()', source)


if __name__ == "__main__":
    unittest.main()
