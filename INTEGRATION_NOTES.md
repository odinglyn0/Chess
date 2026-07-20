# Ender XY + Chess Workflow Integration

This is the repository-ready integration of two previously separate workflows:

1. The JSON chess gantry planner/state machine.
2. The known-working Ender XY web controller's serial method.

## What changed

- `serial.port` can be `"auto"`.
- Fedora `/dev/ttyUSB*` and `/dev/ttyACM*`, macOS `/dev/cu.*`, and Windows `COM*` ports are ranked rather than filtered to macOS only.
- The connector tries the configured baud and fallbacks, normally `115200` then `250000`.
- A port is accepted only after `M115` identifies Marlin.
- Serial bytes are decoded with replacement, so reset noise such as `0xff` cannot crash the program.
- Every command is ASCII, newline terminated, flushed, and acknowledged with `ok` before the next command is sent.
- Manual coordinate commands and JSON chess moves share one persistent serial connection in the browser.
- The original transaction journal, audit log, calibration lock, capture handling, path planning, and atomic state commit remain in place.
- A `diagnose` command performs `M115`, `M119`, and `M114` without moving motors.
- A `web` command exposes manual controls and chess move planning/execution at `127.0.0.1`.

## Main files

- `src/chess_gantry/serial_link.py`: discovery, handshake, transmission, acknowledgements.
- `src/chess_gantry/controller.py`: shared connected controller for manual and chess actions.
- `src/chess_gantry/web_app.py`: local HTTP API and browser UI.
- `src/chess_gantry/service.py`: supports execution over an already-connected link.
- `scripts/run_fedora.sh`: one-command Fedora launcher.

## Test result

Run:

```bash
./scripts/check.sh
```

The integrated version contains 40 automated tests. They include malformed-byte handling, Fedora port discovery, baud fallback, manual coordinates, browser endpoints, JSON planning, and successful persistent-state commit.

## Apply to your clone

Copy the project contents into the root of your `basil-dev` working tree, preserving `.git`, then run:

```bash
git status
./scripts/check.sh
git add .
git commit -m "Integrate Fedora Ender serial and chess gantry web control"
git push origin basil-dev
```

Do not overwrite a real `config.json` or `data/board_state.json` without reviewing them. Those files are intentionally ignored by Git.
