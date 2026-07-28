from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PREFIXES = (
    "node_modules/",
    ".venv/",
    "venv/",
    ".pio/",
    "data/",
)
FORBIDDEN_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
FORBIDDEN_SUFFIXES = (".json.lock", ".gcode", ".pyc")
ALLOWED = {"data/.gitkeep"}


def main() -> int:
    result = subprocess.run(
        ("git", "ls-files", "-z"),
        cwd=ROOT,
        stdout=subprocess.PIPE,
        check=True,
    )
    tracked = [value.decode() for value in result.stdout.split(b"\0") if value]
    invalid = []
    for path in tracked:
        if path in ALLOWED:
            continue
        parts = set(Path(path).parts)
        if (
            path.startswith(FORBIDDEN_PREFIXES)
            or parts.intersection(FORBIDDEN_PARTS)
            or path.endswith(FORBIDDEN_SUFFIXES)
        ):
            invalid.append(path)
    if invalid:
        print("Generated or dependency files are tracked by Git:")
        for path in invalid:
            print(f"  {path}")
        return 1
    print("Git hygiene passed: dependencies and generated runtime files are untracked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
