from __future__ import annotations

from pathlib import Path
import os
import shutil
import sys

from chess_gantry.cli import run


def main() -> int:
    token = os.environ.get("CHESS_GANTRY_WEB_TOKEN", "")
    if len(token) < 24:
        print(
            "CHESS_GANTRY_WEB_TOKEN with at least 24 characters is required.",
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
            "--allow-network",
            "--auth-token",
            token,
            "--no-browser",
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
