# Chess Gantry

Chess Gantry is a Python 3.9+ motion-control framework for a Raspberry Pi connected over USB serial to a Marlin gantry. Physical X and Y receive identical targets to drive the outer gantry; physical E moves the inner carriage independently. The framework accepts a chess move as JSON, validates it against persistent physical board state, plans a collision-aware path, generates G-code, and can execute it on the controller.

The package manages physical consistency, not chess legality. A game engine, Lichess, or another upstream system must decide whether a move is legal before passing it to the gantry.

## Safety first

The example configuration has `safety.calibrated` set to `false`. Planning and demo mode work immediately, but real movement remains locked until the machine has been measured and tested.

- Keep an independent power cutoff accessible whenever the gantry is energized.
- Verify axis directions, endstops, workspace limits, board geometry, speeds, capture slots, and magnet control before setting `safety.calibrated` to `true`.
- Keep Marlin endstops and software limits enabled. The Python workspace check is an additional guard, not a replacement.
- The example magnet commands, `M106 S255` and `M107`, are not universal. Use a correctly rated driver and suitable flyback protection; never drive an electromagnet directly from Raspberry Pi GPIO.
- A valid 2-D path does not prove that real pieces, belts, wiring, or the magnet will clear every obstruction.
- A Marlin `ok` confirms firmware acknowledgement, not successful physical movement. Belt slip, a dropped piece, or magnet failure requires sensing or manual verification.
- `M112` normally requires a controller reset or power cycle followed by re-homing.

## Features

- Flat and nested move-delta JSON with strict validation.
- Persistent, versioned board state keyed by stable piece IDs.
- Normal moves, destination captures, and explicit off-destination captures such as en passant.
- Capture-slot allocation and tracking.
- Configurable board orientation, workspace, feed rates, magnet commands, homing, and parking.
- Direct and occupancy-aware A* path planners.
- Marlin G-code generation with synchronization and magnet dwell times.
- Cross-platform serial discovery, fallback baud probing, `M115` verification, and command-by-command acknowledgement handling.
- Transaction journals, process locking, atomic board-state commits, and audit logging.
- Terminal, browser, UCI, public Lichess PGN, and WebSocket-stream workflows.
- Hardware-free planning, diagnostics, web demo, and motor-test simulation.

## How it works

```text
legal move or game event
        |
        v
move-delta JSON -> validate against stored BoardState
        |
        +-> detect capture and allocate capture slot
        |
        v
board coordinates -> machine millimetres -> path planner
        |
        v
piece transfers -> Marlin G-code
        |
        +-> dry run: print or save only
        |
        v
pending journal -> USB serial -> all commands acknowledged
        |
        v
atomic board-state commit + audit record
```

Persistent state changes only after the complete serial program succeeds. If execution fails or becomes uncertain, the pending journal remains and blocks further execution until the physical board is inspected and reconciled.

## Requirements

- Python 3.9 or newer
- A Python installation with `venv` and `pip`
- For physical execution, a Marlin-compatible controller connected by USB serial
- Optional Docker with Compose for the external Lichess stream service

Python dependencies are installed from `pyproject.toml`:

- `pyserial`
- `websockets`
- `python-chess`

## Installation

Clone the main branch and enter the repository:

```bash
git clone https://github.com/odinglyn0/Chess.git
cd Chess
```

Run the setup script:

```bash
./scripts/install_pi.sh
source .venv/bin/activate
```

The script creates `.venv`, installs the package in editable mode, copies `config.example.json` to `config.json` if needed, and creates `data/board_state.json` from the standard example if needed.

Manual equivalent:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
cp config.example.json config.json
mkdir -p data
cp examples/board_state.standard.json data/board_state.json
```

Runtime files such as `config.json`, board state, journals, audit logs, generated G-code, and Lichess sessions are intentionally ignored by Git.

## Quick start

Activate the environment before using the CLI:

```bash
source .venv/bin/activate
```

Plan a move without opening the serial port or changing board state:

```bash
chess-gantry --config config.json --state data/board_state.json \
  plan examples/move_e2_e4.json
```

Launch the browser controller with simulated hardware:

```bash
chess-gantry --config config.json --state data/board_state.json web --demo
```

It opens at `http://127.0.0.1:8000` by default.

List serial devices and perform a non-moving Marlin diagnostic:

```bash
chess-gantry --config config.json ports
chess-gantry --config config.json diagnose
```

After calibration, execute a move physically:

```bash
chess-gantry \
  --config config.json \
  --state data/board_state.json \
  --journal data/pending_move.json \
  --audit data/audit.jsonl \
  execute examples/move_e2_e4.json \
  --confirm-motion
```

Global options such as `--config`, `--state`, `--journal`, and `--audit` should be placed before the subcommand.

## Move JSON

Coordinates use `x = 0..7` for files `a..h`, `y = 0..7` for ranks `1..8`, and `matrix[y][x]` in matrix integrations.

The original flat format is supported. `position` is the stable physical piece ID:

```json
{
  "event_id": "game-17-ply-23",
  "position": "white_pawn_e",
  "px": 4,
  "py": 1,
  "nx": 4,
  "ny": 3
}
```

`id` may be used instead of `position`, and a nested `position` object is also accepted. `event_id` is optional but recommended; replaying an already processed event is rejected.

A normal destination capture is inferred from persistent board state. En passant and other off-destination captures must identify the captured piece and its actual location:

```json
{
  "event_id": "game-17-ply-31",
  "position": "white_pawn_e",
  "px": 4,
  "py": 4,
  "nx": 3,
  "ny": 5,
  "capture": {
    "id": "black_pawn_d",
    "x": 3,
    "y": 4
  }
}
```

JSON schemas are available in `schemas/move.schema.json` and `schemas/board_state.schema.json`.

## Board state

`data/board_state.json` records every physical piece, its board or capture status, a monotonically increasing revision, and processed event IDs:

```json
{
  "schema_version": 1,
  "revision": 0,
  "pieces": {
    "white_pawn_e": {
      "status": "board",
      "x": 4,
      "y": 1,
      "metadata": {
        "color": "white",
        "kind": "pawn"
      }
    }
  },
  "processed_events": []
}
```

Install or replace an initial state and inspect the active state with:

```bash
chess-gantry --state data/board_state.json init-state examples/board_state.standard.json
chess-gantry --state data/board_state.json show-state
```

Add `--overwrite` to `init-state` only when intentionally replacing an existing state file.

## CLI reference

Both `chess-gantry` and `python -m chess_gantry` invoke the CLI.

| Command                         | Purpose                                                                                                 |
| ------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `plan MOVE`                     | Validate and print G-code without hardware or state mutation. Supports `--output` and `--summary-json`. |
| `validate MOVE`                 | Validate the move, state transition, and planned path without printing G-code.                          |
| `execute MOVE --confirm-motion` | Execute on Marlin and commit state only after success.                                                  |
| `run MOVE`                      | Dry-run by default; add `--confirm-motion` to execute.                                                  |
| `init-state SOURCE`             | Validate and install initial board state; `--overwrite` permits replacement.                            |
| `show-state`                    | Print persistent board state.                                                                           |
| `uci-to-json UCI`               | Convert a four-character move such as `e2e4`; supports `--event-id`, `--en-passant`, and `--output`.    |
| `lichess-event EVENT`           | Convert one saved stream event and plan it; supports move and G-code output paths.                      |
| `lichess-watch GAME_ID`         | Consume WebSocket move events; dry-run by default or execute with explicit confirmation.                |
| `lichess-pgn GAME_ID`           | Fetch and dry-run all currently recorded moves in a public game.                                        |
| `lichess-follow GAME_ID`        | Poll public PGN and generate files for new moves, optionally executing them.                            |
| `ports`                         | List serial devices with likely printer controllers ranked first.                                       |
| `diagnose`                      | Verify Marlin and query endstops and position without movement.                                         |
| `web`                           | Start the browser controller.                                                                           |
| `home --confirm-motion`         | Run the configured coordinate-initialization commands; the shipped configuration performs no homing.    |
| `motor-test`                    | Print the fixed coupled-axis test G-code without opening serial. Add `--confirm-motion` to run it.      |
| `stop`                          | Send the configured emergency-stop command.                                                             |
| `reconcile`                     | Inspect or resolve a pending transaction after checking the physical board.                             |

Get complete options for any command with:

```bash
chess-gantry --help
chess-gantry lichess-follow --help
```

## Configuration and calibration

Edit the generated `config.json`; keep `config.example.json` as a reference. Unknown sections and fields are rejected.

### Serial

The example explicitly uses `/dev/ttyUSB0` at `115200` baud and also permits fallback probing at `250000`. Set `serial.port` to the actual device, or use `"auto"` to rank available serial devices and accept one only after `M115` identifies Marlin.

Opening some USB controllers resets them, so `startup_wait_s` allows firmware startup before probing. Use `diagnose --port PATH --baudrate RATE` to test explicit values without moving motors.

On Linux, if the device exists but access is denied, inspect its group and add your account to that group. Log out and back in afterward:

```bash
stat -c '%n group=%G permissions=%A' /dev/ttyUSB0
sudo usermod -aG dialout "$USER"
```

Replace `dialout` with the group reported on the system.

### Board and workspace

`origin_x_mm` and `origin_y_mm` are the machine coordinates of the centre of logical square `(0, 0)`. Other square centres use `square_size_mm`. Use `flip_x`, `flip_y`, and `swap_xy` to describe how the physical board is mounted rather than altering incoming chess coordinates.

The workspace is the allowed software envelope for magnet-centre coordinates. Board centres, park position, and capture slots must fit within it. Capture slots must be unique and outside the playing area.

### Motion and planner

Configure travel and drag feed rates, magnet dwell times, and optional parking under `motion`.

The default A* planner treats stationary pieces as circular keep-out regions. `obstacle_keepout_mm` must account for the moving piece radius, stationary piece radius, and a safety margin. If no route fits, the move is rejected. The `direct` planner is useful for controlled empty-board tests but intentionally ignores occupied pieces.

### Magnet and safety

Verify the configured magnet commands with the coil disconnected before testing a properly protected, current-limited load. Verify homing and preflight commands against the installed Marlin configuration.

Only set the following after completing physical calibration:

```json
{
  "safety": {
    "calibrated": true
  }
}
```

The real configuration must retain the other required `safety` fields shown in `config.example.json`; the snippet only highlights the lock.

## Browser controller

Start the local controller with:

```bash
chess-gantry --config config.json --state data/board_state.json web
```

The interface supports serial connection, Marlin verification, endstop inspection, homing, guarded manual coordinates, move planning, physical execution, board-state inspection, and emergency stop. Use `--demo` for a simulated controller and `--no-browser` to suppress automatic browser launch.

The server binds only to `127.0.0.1` by default. A non-loopback host requires `--allow-network`. The application provides no authentication or TLS, so do not expose it to an untrusted network.

## Lichess and UCI

### UCI conversion

Convert a move using the current physical board state:

```bash
chess-gantry --config config.json --state data/board_state.json \
  uci-to-json e2e4 --event-id game-17-ply-1 --output data/e2e4.json
```

The UCI adapter supports normal moves, captures, and explicit `--en-passant`. Castling and promotion are rejected because they require physical operations not represented by one standard move delta.

### Public PGN replay

Fetch the current PGN for a public Lichess game, generate JSON and G-code for each move, and advance only an in-memory simulated board:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-pgn GAME_ID
```

Generated files are written to `data/lichess` by default. Persistent board state is not changed.

### Polling a live public game

Poll every five seconds and emit files for newly observed moves:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID
```

Useful options include `--once`, `--interval SECONDS`, `--reset-session`, and the dry-run-only `--obstacle-keepout-mm VALUE`. Hardware execution requires both `--execute` and `--confirm-motion`. Adding `--execute-existing` also runs moves already recorded by a previous dry-run session; it must be used with extreme care.

### WebSocket stream

`lichess-watch` connects by default to `ws://127.0.0.1:8010/ws/GAME_ID`, converts incoming move envelopes, and advances simulated state between planned events. Use `lichess-event` to convert a previously saved event.

The external service under `services/lichess_stream` is currently recorded as a Git submodule that points back to this repository at a pin that is not available from the current public `main` history. Therefore `git submodule update --init --recursive` and `./scripts/start_lichess_stream.sh` may fail. Public `lichess-pgn` and `lichess-follow` do not depend on that service. Repair the submodule pin and service layout before relying on `lichess-watch` or the Docker Compose configuration.

## Outer X/Y and inner E

The two outer-gantry motors use the controller's physical X and Y ports, but their mechanical installation requires opposite shaft directions. Physical X receives the outer coordinate directly; physical Y receives `170 - outer`. The independent inner coordinate is emitted on E. For logical inner `90` and outer `70`:

```gcode
G1 X70 Y100 E90 F600
```

The application continues to use logical `(x, y)` board coordinates internally. At the G-code boundary, logical X maps to physical E, while logical Y maps to physical X directly and physical Y inversely. X and Y always satisfy `X + Y = 170` with the current workspace.

The software now accounts for the mechanically mirrored motor directions. Do not also invert one motor in firmware without rechecking the direction test, or the correction will be applied twice.

Marlin normally treats E as a filament extruder. Gantry programs therefore use `M82` for absolute E positioning and `M302 P1` to permit cold E movement. They restore cold-extrusion protection with `M302 P0` after movement. Do not use this setup with filament loaded or a hotend expecting normal extrusion behavior.

The motor test never issues `G28` and never calls the homing workflow. Its positioning command is `G92 X0 Y350 E0`, which declares the current manually positioned origin without moving a motor.

## Hardware commands

With the complete gantry physically placed at a safe, squared starting position, initialize its current coordinates without movement:

```bash
chess-gantry --config config.json home --confirm-motion
```

First print and inspect the exact sample G-code. This does not open the serial port:

```bash
chess-gantry --config config.json motor-test
```

The sample path is:

```text
inner E: 0 -> 200 -> 0
outer X/Y: 0/350 -> 200/150 -> 0/350
```

You can also pass the program through the in-memory Marlin transport without real hardware:

```bash
chess-gantry --config config.json motor-test --confirm-motion --demo
```

The test moves 20 cm in each mechanical direction. Inner E uses `F3000` at 50 mm/s. Mirrored outer X/Y use `F16971`, which gives each motor approximately 200 mm/s after Marlin applies diagonal vector speed. The test returns each group separately, restores cold-extrusion protection, and ends with `M84`.

Before moving, the test applies matching calibration with a fast outer profile and a controlled inner profile:

```gcode
M82
M302 P1
M92 X80 Y80 E80
M203 X200 Y200 E50
M201 X500 Y500 E300
M205 X5 Y5 E5
```

These set absolute E positioning, permit cold E movement, configure outer X/Y for 200 mm/s, and limit inner E to 50 mm/s. They are session settings and do not require EEPROM persistence.

```bash
chess-gantry --config config.json motor-test --confirm-motion
```

Send the configured emergency stop:

```bash
chess-gantry --config config.json stop
```

The standalone command must open the serial port, so it may not be able to seize a port held by another process. The browser controller sends stop over its existing connection.

## Recovery

Before physical execution, the program writes `data/pending_move.json`. A command error, timeout, crash, or power loss leaves that journal in place and blocks another move.

Inspect the pending transaction:

```bash
chess-gantry --config config.json reconcile
```

After inspecting and, if necessary, manually restoring the physical board, either commit the journal's expected state:

```bash
chess-gantry --config config.json reconcile \
  --mark-applied --confirm-physical-state
```

Or retain the current stored state and discard the journal:

```bash
chess-gantry --config config.json reconcile \
  --discard --confirm-physical-state
```

Never reconcile until stored state and physical reality are known to match one of those outcomes.

## Python integration

```python
import json
from pathlib import Path

from chess_gantry import AppConfig, GantryService, MoveDelta

config = AppConfig.load("config.json")
raw_move = json.loads(Path("incoming_move.json").read_text())
move = MoveDelta.from_mapping(raw_move, config.board.width, config.board.height)

service = GantryService(
    config,
    state_path="data/board_state.json",
    journal_path="data/pending_move.json",
    audit_path="data/audit.jsonl",
)

# Planning neither opens serial nor mutates persistent state.
plan = service.plan(move)
print(plan.program.text())

# Physical execution is locked until safety.calibrated is true.
# service.execute(move)
```

Update an external game matrix only after `execute` returns successfully, or rebuild it from the committed board state. Generating G-code alone is not evidence that the physical move occurred.

## Testing

Install dependencies, then run the full compile and unit-test check:

```bash
./scripts/check.sh
```

Equivalent commands:

```bash
PYTHONPATH=src python -m compileall -q src tests examples
PYTHONPATH=src python -m unittest discover -s tests -v
```

The current suite contains 55 tests covering validation, planning, serial behavior, state transactions, browser APIs, UCI conversion, and Lichess adapters.

## Project layout

```text
Chess/
|-- config.example.json
|-- docker-compose.lichess.yml
|-- examples/
|-- schemas/
|-- scripts/
|-- services/lichess_stream/   # external service submodule; see Lichess note
|-- src/chess_gantry/
|   |-- cli.py
|   |-- config.py
|   |-- controller.py
|   |-- gcode.py
|   |-- kinematics.py
|   |-- lichess_adapter.py
|   |-- lichess_follow.py
|   |-- lichess_pgn.py
|   |-- lichess_watch.py
|   |-- models.py
|   |-- path_planning.py
|   |-- persistence.py
|   |-- serial_link.py
|   |-- service.py
|   |-- uci_adapter.py
|   `-- web_app.py
`-- tests/
```

## Limitations

- Chess legality is intentionally delegated to the upstream game engine.
- A two-axis drag mechanism cannot solve routes physically blocked by tightly packed pieces; smaller pieces, wider spacing, an outside-board corridor, or a lift axis may be required.
- Castling needs two physical transfers and is not accepted as one UCI or Lichess adapter move.
- Promotion needs an external physical replacement process and is rejected by the UCI and Lichess adapters.
- Planner geometry and USB acknowledgements cannot replace physical sensing and supervised calibration.
