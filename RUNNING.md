# Running Chess Gantry

Run all commands from the repository root.

## Install and initialize

Requirements: Python 3.9 or newer. Node.js and npm are only needed for the
formatting and repository-policy checks.

```bash
./scripts/install_pi.sh
source .venv/bin/activate
```

The installer creates `.venv`, installs the Python package in editable mode,
and creates `config.json` and `data/board_state.json` when they do not exist.

Manual equivalent:

```bash
uv sync
cp config.example.json config.json
mkdir -p data
cp examples/board_state.standard.json data/board_state.json
```

For Node-based formatting checks, install the locked development dependencies:

```bash
npm ci
```

## Main program

The installed command and module entry point are equivalent:

```bash
chess-gantry --help
python -m chess_gantry --help
```

Global options such as `--config`, `--state`, `--journal`, and `--audit` must
appear before the subcommand. Use `chess-gantry COMMAND --help` for every
option supported by a command.

### Dry-run a move

Validate a move and print its planned G-code without opening a serial port or
changing persistent board state:

```bash
chess-gantry --config config.json --state data/board_state.json \
  plan examples/move_e2_e4.json
```

Write the G-code to a file and include a JSON summary:

```bash
chess-gantry --config config.json --state data/board_state.json \
  plan examples/move_e2_e4.json --summary-json --output data/move.gcode
```

Validate without printing G-code:

```bash
chess-gantry --config config.json --state data/board_state.json \
  validate examples/move_e2_e4.json
```

The convenience launcher initializes missing local files and dry-runs a move:

```bash
./scripts/run_move.sh
./scripts/run_move.sh examples/move_capture_demo.json
```

`./scripts/run_fedora.sh` provides the same launcher behavior.

### Run the browser controller

Start it with a simulated Marlin controller:

```bash
chess-gantry --config config.json --state data/board_state.json web --demo
```

Start it against configured hardware:

```bash
chess-gantry --config config.json --state data/board_state.json web
```

The default address is `http://127.0.0.1:8000`. Add `--no-browser` to avoid
opening a browser. To bind beyond localhost, supply `--host ADDRESS` and
`--allow-network`; the application has no authentication or TLS.

## Board state

Create the initial state (fails if the destination already exists):

```bash
chess-gantry --state data/board_state.json \
  init-state examples/board_state.standard.json
```

Add `--overwrite` only when intentionally replacing the current stored state.
Print the current state with:

```bash
chess-gantry --state data/board_state.json show-state
```

## Hardware

Real motion is blocked until the machine is calibrated and
`safety.calibrated` is set to `true` in `config.json`. Keep an independent
emergency power cutoff available and inspect generated G-code before moving.

List serial ports and perform a non-moving Marlin diagnostic:

```bash
chess-gantry --config config.json ports
chess-gantry --config config.json diagnose
```

An explicit connection can be tested with:

```bash
chess-gantry --config config.json diagnose \
  --port /dev/ttyUSB0 --baudrate 115200
```

Print the fixed motor-test program without connecting to hardware:

```bash
chess-gantry --config config.json motor-test
```

Exercise the same flow using an in-memory simulated controller:

```bash
chess-gantry --config config.json motor-test --confirm-motion --demo
```

After calibration, run coordinate initialization and the real motor test:

```bash
chess-gantry --config config.json home --confirm-motion
chess-gantry --config config.json motor-test --confirm-motion
```

Execute and commit a physical chess move:

```bash
chess-gantry \
  --config config.json \
  --state data/board_state.json \
  --journal data/pending_move.json \
  --audit data/audit.jsonl \
  execute examples/move_e2_e4.json \
  --confirm-motion
```

The convenience equivalent is:

```bash
./scripts/run_move.sh examples/move_e2_e4.json --confirm-motion
```

Send the configured Marlin emergency-stop command with:

```bash
chess-gantry --config config.json stop
```

## Pending-move recovery

Inspect a journal left by an interrupted or uncertain physical move:

```bash
chess-gantry --config config.json reconcile
```

After physically verifying the board, either commit the expected next state:

```bash
chess-gantry --config config.json reconcile \
  --mark-applied --confirm-physical-state
```

Or keep the current stored state and remove the journal:

```bash
chess-gantry --config config.json reconcile \
  --discard --confirm-physical-state
```

## UCI and Lichess

Convert a UCI move to native move JSON:

```bash
chess-gantry --config config.json --state data/board_state.json \
  uci-to-json e2e4 --event-id game-17-ply-1 --output data/e2e4.json
```

Fetch a public Lichess game's current PGN and dry-run all recorded moves:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-pgn GAME_ID --output-dir data/lichess
```

Stream a public game in real time and create JSON/G-code for new moves as they
are played:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID --output-dir data/lichess
```

Useful variants:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID --once
chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID --interval 10
```

`--once` processes the current game state a single time and exits. `--interval`
is the delay in seconds before reconnecting a dropped stream.

Physical execution of followed moves requires explicit opt-in:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID --execute --confirm-motion
```

Following streams directly from `https://lichess.org` through the official
`berserk` client. No stream service, container, or submodule is required. To
raise rate limits or read your own games, export a personal token first:

```bash
export LICHESS_TOKEN="lip_xxxxxxxxxxxxxxxx"
```

## Tests and checks

Run Python compilation and the complete unit-test suite:

```bash
./scripts/check.sh
```

Equivalent commands:

```bash
PYTHONPATH=src uv run python -m compileall -q src tests examples
PYTHONPATH=src uv run python -m unittest discover -s tests -v
```

Run one test module, class, or method by dotted name:

```bash
PYTHONPATH=src uv run python -m unittest tests.test_controller -v
PYTHONPATH=src uv run python -m unittest \
  tests.test_controller.ControllerTests.test_method_name -v
```

Run all repository formatting and policy checks (requires `npm ci` first):

```bash
npm run check
```

Check or apply formatting separately:

```bash
npm run format:check
npm run format
```

Run only the repository policy check:

```bash
npm run steering:check
```
