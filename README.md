# Chess Gantry

Chess Gantry turns chess moves into collision-aware G-code for a Cartesian,
Marlin-controlled gantry. It can plan moves without hardware, drive a real
machine over USB serial, maintain the physical board state, and consume moves
from UCI or Lichess.

The project is designed for a Raspberry Pi and a magnetic chess-piece gantry,
but its planning and demo workflows run on any system with Python 3.9 or newer.

## Features

- Validates flat or nested move JSON against per-game board state
- Plans direct or A* paths around occupied squares
- Handles normal moves, captures, en passant, and capture storage slots
- Generates Marlin G-code with configurable motion and magnet commands
- Discovers serial devices, probes baud rates, and verifies Marlin with `M115`
- Commits board state, recovery journals, and audit logs to Redis per game
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

The installer creates the virtual environment and installs the package in
editable mode. Deployment state is initialized automatically in Redis when a
game is first seen.

Start Redis and plan the included `e2` to `e4` example without connecting to
hardware:

```bash
docker compose -f docker-compose.lichess.yml up -d redis
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  --game-id local-demo \
  plan examples/move_e2_e4.json
```

Or launch the browser controller with a simulated Marlin device:

```bash
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  --game-id local-demo web --demo
```

Open <http://127.0.0.1:8000> if the browser does not open automatically.

For a manual installation:

```bash
uv sync
cp config.example.json config.json
mkdir -p data
docker run -d --name chess-redis -p 6379:6379 redis:7-alpine
```

## Run everything

`uv sync` creates `.venv`. Run commands from the repository root either through
`uv run` or with that environment activated:

```bash
uv run chess-gantry --help
uv run chess-gantry COMMAND --help
```

Global options must precede the command. For example, use
`chess-gantry --config config.json --game-id demo plan MOVE.json`, not
`chess-gantry plan --config ...`.

### Choose state storage

Redis is the recommended mode. Start it once, then give every command a game
ID:

```bash
docker compose -f docker-compose.lichess.yml up -d redis

chess-gantry --config config.json \
  --redis-url redis://localhost:6379/0 \
  --game-id demo \
  show-state
```

Each game ID has independent board state, recovery data, and audit history. A
new game ID starts with the standard 8×8 position. Stop Redis with
`docker compose -f docker-compose.lichess.yml stop redis`; remove its persistent
volume only when you intentionally want to erase all locally stored games.

Local JSON files remain available for a self-contained development run:

```bash
chess-gantry --config config.json \
  --state data/board_state.json \
  --journal data/pending_move.json \
  --audit data/audit.jsonl \
  show-state
```

The `--state`, `--journal`, and `--audit` flags already default to those paths,
so they may be omitted. `./scripts/run_move.sh` and
`./scripts/run_fedora.sh` use this file-backed mode.

For Upstash REST, keep credentials in deployment secrets:

```bash
export UPSTASH_REDIS_REST_URL="https://your-database.upstash.io"
export UPSTASH_REDIS_REST_TOKEN="your-rotated-token"
chess-gantry --config config.json --game-id GAME_ID show-state
```

Never commit the REST token or pass it as a command-line argument. Redis keys
are namespaced by game ID. On a Lichess `game_over` event, game data receives
the `--completed-game-ttl` expiry, which defaults to 86,400 seconds.

### Run a game

Chess Gantry is a physical move executor, not a chess clock, user interface, or
rules engine. A game is a sequence of upstream moves. For every move, the
gantry verifies that its stored physical-board state matches the source square,
plans a collision-free transfer, generates G-code, optionally sends it to
Marlin, and commits the next state only after successful physical execution.

For a local or custom game:

1. Put every physical piece in the standard starting position.
2. Start Redis and choose a new, stable game ID. Do not reuse an ID from an
   unrelated game.
3. Dry-run the first move and inspect its plan.
4. Diagnose and test the machine.
5. Execute each move JSON in turn, always using the same game ID.

```bash
source .venv/bin/activate
docker compose -f docker-compose.lichess.yml up -d redis

export CHESS_GAME_ID="local-2026-07-24-a"

# A new ID automatically receives the standard starting state.
chess-gantry --config config.json \
  --redis-url redis://localhost:6379/0 \
  --game-id "$CHESS_GAME_ID" show-state

# Rehearse the move. This does not alter stored state.
chess-gantry --config config.json \
  --redis-url redis://localhost:6379/0 \
  --game-id "$CHESS_GAME_ID" \
  plan examples/move_e2_e4.json --summary-json

# Execute it. State advances only after Marlin acknowledges the whole program.
chess-gantry --config config.json \
  --redis-url redis://localhost:6379/0 \
  --game-id "$CHESS_GAME_ID" \
  execute examples/move_e2_e4.json --confirm-motion

# Confirm the committed physical-board model.
chess-gantry --config config.json \
  --redis-url redis://localhost:6379/0 \
  --game-id "$CHESS_GAME_ID" show-state
```

Create subsequent JSON with `uci-to-json`, or accept JSON from another chess
application. The upstream application must enforce legal chess moves. Castling
and promotion are deliberately rejected because they require multi-piece or
piece-replacement workflows. Normal moves, ordinary captures, and en passant
are supported.

### Tests, formatting, and repository checks

Run the complete Python test suite and byte-compile the source:

```bash
./scripts/check.sh
```

Run one test module or one specific test:

```bash
PYTHONPATH=src uv run python -m unittest tests.test_controller -v
PYTHONPATH=src uv run python -m unittest \
  tests.test_controller.ControllerTests.test_method_name -v
```

Install the locked Node tooling once, then run every formatting and repository
policy check:

```bash
npm ci
npm run check
```

The individual developer commands are:

```bash
npm run format:check   # check formatting without changing files
npm run steering:check # check repository policy
npm run format         # rewrite files to the required format
```

`npm run format` changes files. The installed Git pre-commit and pre-push hooks
run the corresponding checks automatically.

### Dry runs, simulations, and physical tests

Use this test ladder in order. The first four levels do not move real hardware:

```bash
# 1. Software regression test: no hardware or Redis required.
./scripts/check.sh

# 2. Validate the input, state, and path; produce no G-code.
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  --game-id demo validate examples/move_e2_e4.json

# 3. Dry-run the complete planner and print the exact G-code.
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  --game-id demo plan examples/move_e2_e4.json

# Save the G-code and print the plan summary.
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  --game-id demo plan examples/move_e2_e4.json \
  --summary-json --output data/e2e4.gcode

# 4a. Print the fixed mechanical-test G-code without connecting.
chess-gantry --config config.json motor-test

# 4b. Exercise command streaming against an in-memory Marlin simulation.
chess-gantry --config config.json motor-test --confirm-motion --demo

# The browser workflow can use the same simulated transport.
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  --game-id demo web --demo

# 5. Read-only physical-controller tests: opens serial but does not move.
chess-gantry --config config.json ports
chess-gantry --config config.json diagnose

# 6. Guarded real movement, only after calibration and clearance checks.
chess-gantry --config config.json motor-test --confirm-motion
```

`validate` and `plan` do not open serial, create a recovery transaction, commit
board state, or move a piece. `motor-test --demo` opens no serial port and does
not alter chess state. `diagnose` opens the real port, verifies Marlin with
`M115`, and reads `M119` and `M114`, but sends no movement command.

The real motor test is independent of chess state. It defines the configured
coordinates, forces the magnet off, moves the outer X/Y group and inner E
group through a fixed test program, waits for acknowledgements, and disables
the steppers. It requires `safety.calibrated: true`; inspect the printed dry-run
program first and keep the physical emergency cutoff within reach.

`./scripts/run_move.sh MOVE.json` is another file-backed dry-run shortcut.
Adding `--confirm-motion` changes it into a real execution, so do not add that
flag during rehearsal.

The browser controller defaults to <http://127.0.0.1:8000>. Add
`--no-browser` for a headless run or `--web-port PORT` to change the port. A
non-loopback `--host` also requires `--allow-network`; the controller does not
provide authentication or TLS.

### Board state and move conversion

```bash
# Display the current board.
chess-gantry --redis-url redis://localhost:6379/0 --game-id demo show-state

# Replace a file-backed state from an example (destructive to that state file).
chess-gantry --state data/board_state.json init-state \
  examples/board_state.standard.json --overwrite

# Convert legal UCI notation to native move JSON.
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  --game-id demo uci-to-json e2e4 \
  --event-id demo-ply-1 --output data/e2e4.json
```

Use a fresh game ID when replaying examples from the initial position. Planning
does not advance state; successful physical execution does.

### Hardware diagnostics and actual motion

First inspect `config.json`, calibrate the workspace, set `safety.calibrated`
to `true`, clear the physical board area, and keep an independent emergency
power cutoff available.

```bash
# Enumerate likely serial devices.
chess-gantry --config config.json ports

# Connect, identify Marlin with M115, then read endstops and position.
chess-gantry --config config.json diagnose
chess-gantry --config config.json diagnose \
  --port /dev/ttyUSB0 --baudrate 115200

# Initialize the configured coordinates on real hardware.
chess-gantry --config config.json home --confirm-motion

# Send the fixed real-hardware motor test.
chess-gantry --config config.json motor-test --confirm-motion

# Execute a chess move and commit its new board state.
chess-gantry --config config.json \
  --redis-url redis://localhost:6379/0 \
  --game-id GAME_ID \
  execute examples/move_e2_e4.json --confirm-motion

# File-backed convenience equivalent.
./scripts/run_move.sh examples/move_e2_e4.json --confirm-motion

# Send the configured Marlin emergency-stop command.
chess-gantry --config config.json stop
```

`--confirm-motion` is the explicit opt-in for physical movement. `stop` opens
the configured hardware connection and Marlin normally requires a reset
afterward.

If execution is interrupted and leaves a recovery journal, inspect it:

```bash
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  --game-id GAME_ID reconcile
```

After physically checking the board, either commit the journal's expected state
or discard the journal while retaining the stored state:

```bash
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  --game-id GAME_ID reconcile --mark-applied --confirm-physical-state

chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  --game-id GAME_ID reconcile --discard --confirm-physical-state
```

### Lichess

Use `lichess-follow` for the normal Lichess-to-gantry workflow. It polls the
public PGN, converts every ply to stable native move JSON, plans it against the
expected position, and records `.json`, `.gcode`, and `.session.json` files.
The Lichess game ID automatically becomes the Redis game namespace, so a
separate global `--game-id` is not required.

Copy `GAME_ID` from a URL such as `https://lichess.org/GAME_ID`. The game must
be publicly exportable; this command does not create a Lichess game, submit
moves, operate a player account, or use a bot token.

#### Rehearse a Lichess game

Start with a new output directory or reset its session deliberately:

```bash
# Inspect all moves currently in the PGN without creating a follow session.
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  lichess-pgn GAME_ID --output-dir data/lichess

# Create the follow session and dry-run each currently available move once.
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  lichess-follow GAME_ID \
  --output-dir data/lichess/GAME_ID \
  --once

# Continue watching; new moves are checked every five seconds.
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  lichess-follow GAME_ID \
  --output-dir data/lichess/GAME_ID
```

Dry-run following does not advance Redis board state. The session file only
remembers which output files were emitted; it is not the physical-board state.
Use `--interval SECONDS` to change polling frequency. To deliberately forget
the emitted-file history and regenerate the plans:

```bash
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  lichess-follow GAME_ID \
  --output-dir data/lichess/GAME_ID \
  --once --reset-session
```

For a dry-run-only clearance experiment, add
`--obstacle-keepout-mm MILLIMETRES`. That temporary override cannot be combined
with `--execute`.

#### Physically run a Lichess game

The supported safe synchronization model is:

- the physical board begins in the standard position;
- the Redis namespace for this Lichess ID is new and therefore also standard;
- the follower executes every Lichess ply in order;
- the same command remains running to execute later moves.

For a game that already has moves, this means putting the physical pieces back
at the standard start and allowing the gantry to replay the recorded moves.
Do not point a fresh standard Redis state at a manually arranged mid-game
board. The program cannot infer that physical position.

After completing the physical-test ladder:

```bash
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  lichess-follow GAME_ID \
  --output-dir data/lichess/GAME_ID-physical \
  --execute --confirm-motion
```

On its first poll, a fresh physical session executes all currently recorded
plies in order. It then polls for and executes new plies. Each successful ply
updates Redis; a failure leaves a recovery journal and stops progress until the
operator reconciles the real board.

If the same output session was previously used for a dry run, historical plies
are marked as emitted and are skipped by physical mode. `--execute-existing`
overrides that protection, but use it only when the physical board and Redis
state are both at that session's saved base position. A clearer and safer
normal practice is a separate fresh `GAME_ID-physical` output directory, as
shown above.

Stop following with `Ctrl+C`. Restart with the same Redis game ID and physical
output directory to continue; processed event IDs prevent successfully
committed plies from executing twice. When the PGN reports a final result, the
follower exits and applies the completed-game Redis expiry.

`lichess-pgn` is always a dry run. It replays the exported PGN in memory and
writes plans, but neither changes Redis state nor follows future moves.

#### Optional WebSocket route

The alternative WebSocket pipeline uses the optional Lichess stream submodule:

```bash
git submodule update --init --recursive
./scripts/start_lichess_stream.sh

chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  lichess-watch GAME_ID --output-dir data/lichess
```

`start_lichess_stream.sh` uses Docker Compose when available and otherwise
creates a service-specific virtual environment. The default stream URL is
`ws://127.0.0.1:8010`. Add `--execute --confirm-motion` to `lichess-watch` only
for a calibrated physical run.

To process one previously saved stream event without starting the service:

```bash
chess-gantry --config config.json --redis-url redis://localhost:6379/0 \
  --game-id demo \
  lichess-event examples/lichess_e2_e4_event.json \
  --move-output data/lichess_e2e4.json \
  --gcode-output data/lichess_e2e4.gcode
```

## How it works

```text
move JSON / UCI / Lichess PGN or WebSocket event
                         |
                         v
          normalize to native MoveDelta JSON
                         |
                         v
        load per-game physical state from Redis
                         |
                         v
       validate source, destination, and capture
                         |
                         v
       direct path or obstacle-aware A* planning
                         |
                         v
       board coordinates -> machine coordinates
                         |
                         v
         magnet and motion Marlin G-code
                    /               \
                   v                 v
        dry run: print/save     physical execution
        no state mutation       create recovery journal
                                      |
                                      v
                           stream one command at a time
                           wait for each Marlin `ok`
                                      |
                         +------------+------------+
                         |                         |
                      success                   failure
                         |                         |
                         v                         v
                atomically commit state     retain old state and
                clear journal, audit        recovery journal
```

The stored state models the physical board, including stable piece IDs, occupied
squares, capture slots, revision number, and processed event IDs. Captures are
planned as two transfers: captured piece to an available storage slot, then the
moving piece to its destination. En passant uses its explicit off-destination
capture square.

During execution, the recovery journal records the current state, intended next
state, move, and G-code before motion starts. Board state is committed only
after every command is acknowledged. If communication or motion becomes
uncertain, the journal prevents more planning until an operator physically
checks the board and runs `reconcile`.

Chess Gantry manages physical consistency; it is not a chess engine. Lichess or
another upstream application adjudicates move legality. Planning answers “can
the configured gantry route this known move through the modeled physical
position?”; it does not answer “is this chess move legal?”

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
