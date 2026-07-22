# Chess Gantry

Chess Gantry turns chess moves into collision-aware G-code for a Cartesian,
Marlin-controlled gantry. It can plan moves without hardware, drive a real
machine over USB serial, maintain the physical board state, and consume moves
from UCI or Lichess.

The project is designed for a Raspberry Pi and a magnetic chess-piece gantry,
but its planning and demo workflows run on any system with Python 3.9 or newer.

## Features

- Validates flat or nested move JSON against persistent board state
- Plans direct or A* paths around occupied squares
- Handles normal moves, captures, en passant, and capture storage slots
- Generates Marlin G-code with configurable motion and magnet commands
- Discovers serial devices, probes baud rates, and verifies Marlin with `M115`
- Commits board state transactionally with recovery journals and audit logs
- Includes a local browser controller and an in-memory hardware demo
- Converts UCI moves and follows public Lichess games

> [!WARNING]
> Moving hardware can cause injury or damage. Keep an independent emergency
> power cutoff available, verify the generated G-code, and calibrate the
> workspace before enabling physical execution. The example configuration has
> `safety.calibrated` set to `false` intentionally.

## Quick start

Clone the repository, then install and initialize the local environment:

```bash
./scripts/install_pi.sh
source .venv/bin/activate
```

The installer creates the virtual environment, installs the package in editable
mode, and initializes `config.json` and `data/board_state.json` if needed.

Plan the included `e2` to `e4` example without connecting to hardware:

```bash
chess-gantry --config config.json --state data/board_state.json \
  plan examples/move_e2_e4.json
```

Or launch the browser controller with a simulated Marlin device:

```bash
chess-gantry --config config.json --state data/board_state.json web --demo
```

Open <http://127.0.0.1:8000> if the browser does not open automatically.

For a manual installation:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
cp config.example.json config.json
mkdir -p data
cp examples/board_state.standard.json data/board_state.json
```

## Common commands

Global options such as `--config` and `--state` must appear before the
subcommand.

```bash
# Validate a move and its planned path
chess-gantry --config config.json --state data/board_state.json \
  validate examples/move_e2_e4.json

# Inspect the stored physical board state
chess-gantry --state data/board_state.json show-state

# Convert a legal UCI move to the native JSON format
chess-gantry --config config.json --state data/board_state.json \
  uci-to-json e2e4

# List candidate serial ports and run non-moving diagnostics
chess-gantry --config config.json ports
chess-gantry --config config.json diagnose

# Show every command and option
chess-gantry --help
```

### Execute a physical move

After reviewing `config.json`, calibrating the machine, setting
`safety.calibrated` to `true`, and clearing the workspace:

```bash
chess-gantry \
  --config config.json \
  --state data/board_state.json \
  --journal data/pending_move.json \
  --audit data/audit.jsonl \
  execute examples/move_e2_e4.json \
  --confirm-motion
```

The explicit `--confirm-motion` flag prevents accidental actuation. Use
`chess-gantry --config config.json stop` to send the configured emergency-stop
command.

### Follow a Lichess game

Fetch a public game's current PGN and generate move JSON and G-code:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-pgn GAME_ID --output-dir data/lichess
```

Poll for new moves continuously:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID --output-dir data/lichess
```

These commands plan moves by default. Physical execution requires both
`--execute` and `--confirm-motion`.

## How it works

```text
move JSON / UCI / Lichess
            |
            v
 board-state validation
            |
            v
 direct or A* path planning
            |
            v
     Marlin G-code
        /       \
   dry run     serial execution
                    |
                    v
          atomic state commit
```

Chess Gantry manages physical consistency; it is not a chess engine. Upstream
software should adjudicate move legality before handing a move to the gantry.

Configuration lives in `config.json`. Start from `config.example.json` and
review the board geometry, workspace limits, feed rates, magnet commands,
planner settings, capture slots, homing sequence, and safety controls for your
machine.

## Move and state formats

JSON schemas are available in [`schemas/move.schema.json`](schemas/move.schema.json)
and [`schemas/board_state.schema.json`](schemas/board_state.schema.json). Ready-to-run
examples live in [`examples/`](examples/), including normal moves, captures,
and en passant.

## Development

Run compilation and the complete unit-test suite:

```bash
./scripts/check.sh
```

Formatting and repository-policy checks additionally require Node.js:

```bash
npm ci
npm run check
```

The Python package uses a `src/` layout. The main components are:

- `service.py` and `controller.py` for orchestration and transaction handling
- `path_planning.py`, `kinematics.py`, and `gcode.py` for motion planning
- `serial_link.py` for Marlin discovery and acknowledged command streaming
- `web_app.py` for the local browser interface
- `lichess_*.py` and `uci_adapter.py` for external move sources

## Documentation

- [`RUNNING.md`](RUNNING.md) — complete command and operational reference
- [`INTEGRATION_NOTES.md`](INTEGRATION_NOTES.md) — serial and web integration notes
- [`LICHESS_PIPELINE.md`](LICHESS_PIPELINE.md) — WebSocket-based Lichess pipeline
- [`TEST_REPORT.txt`](TEST_REPORT.txt) — recorded verification details
