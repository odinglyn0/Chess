from __future__ import annotations

from pathlib import Path
import os
import shutil
import sys

from chess_gantry.cli import run


def main() -> int:
    if not os.environ.get("CLERK_PUBLISHABLE_KEY", "").strip():
        print(
            "CLERK_PUBLISHABLE_KEY is required; the dashboard has no other way to"
            " authenticate anyone.",
            file=sys.stderr,
        )
        return 2
    data = Path("/app/data")
    data.mkdir(parents=True, exist_ok=True)
    state = data / "board_state.json"
    if not state.exists():
        shutil.copyfile("/app/examples/board_state.standard.json", state)
    return run(
        (
            "--config",
            "/app/config.json",
            "--state",
            str(state),
            "--journal",
            str(data / "pending_move.json"),
            "--audit",
            str(data / "audit.jsonl"),
            "web",
            "--host",
            "0.0.0.0",
            "--web-port",
            "8000",
            "--no-browser",
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
