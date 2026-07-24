# Chess Gantry

Chess Gantry converts chess moves into collision-aware Marlin G-code for a
magnetic Cartesian gantry. It can:

- plan and execute piece transfers
- avoid occupied squares with A* path planning
- control an electromagnet through Marlin fan outputs
- run fixed movement, magnet, and full-board sweep tests
- mirror public Lichess games in near real time
- provide a local browser controller
- recover safely from interrupted physical moves

All state is stored in local JSON and JSONL files. There is no Redis, Upstash,
database server, or cloud state dependency.

## Important Safety Status

> [!WARNING]
> Moving gantries and electromagnets can cause injury, overheating, controller
> resets, or hardware damage. Keep an independent emergency power cutoff within
> reach. Never leave an energized electromagnet unattended.

The software and simulated workflows pass their automated checks. Physical
operation still depends on correct measurements, wiring, current limits, and
mechanical clearance.

Known physical findings:

- The Ender controller was detected as `/dev/ttyUSB0` at 115200 baud.
- The controller accepted movement, endstop, position, and fan commands.
- Its firmware acknowledges `M115` without returning a Marlin identity, so
  `config.json` uses `verify_marlin: false` while still requiring command
  acknowledgements.
- The electromagnet is configured to drive logical fan indices `P0` and `P1`
  at full PWM because the Ender connector label does not necessarily match the
  logical Marlin fan number.
- A physical test with the electromagnet directly attached caused the USB or
  controller connection to reset under load.
- After that event, `/dev/ttyUSB0` temporarily disappeared. Always run
  `diagnose` before a presentation.

The configured magnet commands are:

```gcode
M106 P0 S255
M106 P1 S255
```

Both outputs are disabled with:

```gcode
M107 P0
M107 P1
```

If energizing the magnet resets the controller, do not repeatedly retry it.
Drive the magnet through a correctly rated MOSFET or relay module with flyback
protection and an appropriate external supply. Use the Ender output as a control
signal and share ground where required by the driver design.

## Install

Run from the repository root:

```bash
uv sync
npm ci
```

The main executable is run through `uv`:

```bash
uv run chess-gantry --help
```

## Verify Everything

Run the Python compilation and unit suite:

```bash
./scripts/check.sh
```

Run formatting and repository policy checks:

```bash
npm run check
```

Run the complete simulated demo-readiness workflow:

```bash
./scripts/demo_check.sh
```

This performs:

- Python compilation
- all automated tests
- Black and Prettier checks
- repository policy checks
- an `e2` to `e4` planning test
- a simulated electromagnet test
- a simulated 64-square board sweep

No physical serial port is opened by `demo_check.sh`.

## Simulated Browser Demo

Launch the complete browser UI against simulated Marlin:

```bash
./scripts/live_demo.sh
```

Open <http://127.0.0.1:8000> and stop the server with `Ctrl+C`.

The browser demo uses:

```text
config.demo.json
data/demo/board_state.json
data/demo/pending_move.json
data/demo/audit.jsonl
```

It does not open the Ender serial port or modify physical-game state.

## Presentation Movement Demo

The presentation mode repeats a fixed four-leg path while keeping both fan
outputs at full power. It refreshes both `M106 ... S255` commands before every
movement leg and sends no `M107` until the final return.

### 1. Print The G-code

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 20 \
  --feed-mm-min 1200 \
  --magnet-on \
  --presentation-loops 3
```

Printing is a dry run. It does not open the serial port.

### 2. Simulate The Presentation

```bash
uv run chess-gantry --config config.demo.json motor-test \
  --distance-mm 20 \
  --feed-mm-min 1200 \
  --magnet-on \
  --presentation-loops 3 \
  --confirm-motion \
  --confirm-magnet \
  --demo
```

### 3. Check The Physical Controller

Reconnect controller power and USB, then run:

```bash
uv run chess-gantry --config config.json ports
uv run chess-gantry --config config.json diagnose
```

Do not continue unless `diagnose` connects successfully and reports endstop and
position data.

### 4. Run The Physical Presentation

Before running:

- put the gantry at the configured coordinate origin
- put one piece directly beneath the electromagnet
- clear the complete 20 mm by 20 mm path
- verify the direction and scale with a movement-only test
- keep the emergency power cutoff ready
- verify that energizing the magnet no longer resets the controller

Then run:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 20 \
  --feed-mm-min 1200 \
  --magnet-on \
  --presentation-loops 3 \
  --confirm-motion \
  --confirm-magnet
```

The path is repeated three times:

```text
origin -> inner +20 mm -> outer +20 mm -> inner origin -> outer origin
```

Presentation mode:

- keeps the magnet on through all movement loops
- refreshes `P0` and `P1` at `S255` before each leg
- turns both outputs off after the final movement
- disables motors after completion
- performs best-effort magnet and motor shutdown after a serial failure
- rejects configurations whose estimated energized movement exceeds 30 seconds
- does not modify chess board-state JSON

## Hardware Test Ladder

Run these in order after entering measured machine geometry.

### Controller Discovery

```bash
uv run chess-gantry --config config.json ports
uv run chess-gantry --config config.json diagnose
```

### Movement Only

Print a short test:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 5 --feed-mm-min 300
```

Run it physically:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 5 --feed-mm-min 300 --confirm-motion
```

Increase only after verifying direction, scale, clearance, and return position:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 20 --feed-mm-min 1200 --confirm-motion
```

### Electromagnet Only

Print a one-second pulse:

```bash
uv run chess-gantry --config config.json magnet-test --duration-s 1
```

Simulate it:

```bash
uv run chess-gantry --config config.demo.json magnet-test \
  --duration-s 1 --confirm-motion --demo
```

Run it physically only after correcting any load-induced reset:

```bash
uv run chess-gantry --config config.json magnet-test \
  --duration-s 1 --confirm-motion
```

The command sends both outputs off before the pulse, drives both at full PWM,
and sends both outputs off afterward. Magnet-only pulses are limited to five
seconds.

### Pickup, Move, Release, Return

Print the sequence:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 20 --feed-mm-min 1200 --magnet-on
```

Run it physically:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 20 --feed-mm-min 1200 --magnet-on \
  --confirm-motion --confirm-magnet
```

This mode picks up at the origin, holds through the two outbound movement legs,
releases at the destination, and returns to the origin with the magnet off.

## Full-Board Sweep

Generate a serpentine sweep over all 64 square centers without connecting:

```bash
uv run chess-gantry --config config.json board-sweep \
  --feed-mm-min 1800 \
  --magnet-on \
  --output data/board-sweep.gcode
```

Simulate it:

```bash
uv run chess-gantry --config config.demo.json board-sweep \
  --feed-mm-min 1800 \
  --magnet-on \
  --confirm-motion \
  --demo
```

For physical execution, remove every piece and obstruction, place the gantry at
the configured origin, inspect the generated G-code, then run:

```bash
uv run chess-gantry --config config.json board-sweep \
  --feed-mm-min 1800 \
  --magnet-on \
  --confirm-motion \
  --confirm-empty-board \
  --confirm-origin \
  --confirm-magnet
```

The sweep pulses the configured magnet outputs for 300 ms at each square and
turns them off during travel. The feed cannot exceed
`motion.travel_feed_mm_min`.

## Physical Calibration

The panel is 500 x 600 mm, but panel dimensions do not define safe tool-center
travel.

The checked-in physical `config.json` still contains:

```json
"square_size_mm": 0.05
```

That is not a usable physical chess-square pitch. Do not run physical chess
moves or a full-board sweep until these values are measured and updated:

- `workspace.min_x_mm`
- `workspace.max_x_mm`
- `workspace.min_y_mm`
- `workspace.max_y_mm`
- `board.square_size_mm`
- `board.origin_x_mm` and `board.origin_y_mm`, representing the center of `a1`
- `board.flip_x`, `board.flip_y`, and `board.swap_xy`
- `motion.park_x_mm` and `motion.park_y_mm`
- every `capture.slots` coordinate
- `safety.home_commands`
- safe travel and drag feed limits

`config.demo.json` models a simulated 500 x 600 workspace with 50 mm squares.
Its coordinates are not physical calibration measurements.

A value of `safety.calibrated: true` is an operator assertion, not proof that
the configuration matches the machine.

## Plan And Execute A Move

Validate and print G-code without moving hardware:

```bash
uv run chess-gantry --config config.json \
  plan examples/move_e2_e4.json --summary-json
```

Validate without printing G-code:

```bash
uv run chess-gantry --config config.json \
  validate examples/move_e2_e4.json
```

Execute after physical calibration:

```bash
uv run chess-gantry --config config.json \
  execute examples/move_e2_e4.json --confirm-motion
```

Convert a legal UCI move to move JSON:

```bash
uv run chess-gantry --config config.json \
  uci-to-json e2e4 --event-id manual-1 --output data/manual-1.json
```

The upstream game source must enforce chess legality. The planner validates
state consistency, occupied squares, workspace bounds, paths, and capture-slot
availability.

## JSON State

Default local files:

```text
data/board_state.json
data/pending_move.json
data/audit.jsonl
```

Their roles are:

- `board_state.json`: piece positions, revision, and processed event IDs
- `pending_move.json`: crash-recovery transaction for an in-progress move
- `audit.jsonl`: append-only operation history

Writes are atomic and protected by local file locks. A physical move is only
committed to `board_state.json` after Marlin acknowledges the complete program.
An interrupted move leaves `pending_move.json` in place and blocks later moves
until the board is reconciled.

Show local state:

```bash
uv run chess-gantry --config config.json show-state
```

Reset only after physically restoring every piece to its standard position:

```bash
uv run chess-gantry --config config.json reset-state \
  --confirm-standard-position
```

Never reset while a movement or game follower is running.

## Lichess Game `6RkOwfp1`

The helper script defaults to game ID:

```text
6RkOwfp1
```

Its files live under:

```text
data/lichess/6RkOwfp1/
```

Typical contents:

```text
board_state.json
pending_move.json
audit.jsonl
dry-run.session.json
physical.session.json
dry-run/*.json
dry-run/*.gcode
physical/*.json
physical/*.gcode
replay/*.json
replay/*.gcode
```

### Check The Public Game

Run all readiness checks and replay its current public PGN without hardware:

```bash
./scripts/lichess_game.sh check
```

At the latest validation, `6RkOwfp1` was publicly reachable and contained zero
moves, which is valid for a game that has not started.

### Follow Without Hardware

Start this before the first move:

```bash
./scripts/lichess_game.sh dry-run
```

The follower polls every two seconds and writes move JSON and G-code. Stop it
with `Ctrl+C`.

### Inspect Or Reset Its State

```bash
./scripts/lichess_game.sh status
./scripts/lichess_game.sh reconcile
```

Physically restore the standard board before resetting:

```bash
./scripts/lichess_game.sh reset
```

### Play Physically

Only after calibration and the hardware test ladder pass:

```bash
./scripts/lichess_game.sh reset
./scripts/lichess_game.sh play
```

Leave `play` running. It mirrors both players' new moves and commits JSON state
only after successful movement.

The public PGN follower supports:

- normal moves
- captures
- en passant
- kingside and queenside castling as ordered king and rook transfers

Promotion is rejected because physical piece replacement is not implemented.
The software observes public games; it does not create games, submit moves,
press a clock, or control a Lichess account.

Use another public game ID as the second argument:

```bash
./scripts/lichess_game.sh check OTHER_GAME_ID
./scripts/lichess_game.sh dry-run OTHER_GAME_ID
./scripts/lichess_game.sh play OTHER_GAME_ID
```

## Recovery

Inspect a local pending transaction:

```bash
uv run chess-gantry --config config.json reconcile
```

If the physical move completed exactly as recorded:

```bash
uv run chess-gantry --config config.json reconcile \
  --mark-applied --confirm-physical-state
```

If the move did not complete and the board still matches `board_state.json`:

```bash
uv run chess-gantry --config config.json reconcile \
  --discard --confirm-physical-state
```

For game `6RkOwfp1`, use its isolated paths:

```bash
uv run chess-gantry \
  --config config.json \
  --state data/lichess/6RkOwfp1/board_state.json \
  --journal data/lichess/6RkOwfp1/pending_move.json \
  --audit data/lichess/6RkOwfp1/audit.jsonl \
  reconcile
```

Never delete a pending journal without checking the physical board.

## Emergency Stop

Send the configured Marlin emergency-stop command:

```bash
uv run chess-gantry --config config.json stop
```

Marlin normally requires a controller reset afterward. This command is not a
substitute for an independent physical power cutoff.

## Browser Controller

Simulated browser controller:

```bash
./scripts/live_demo.sh
```

Physical browser controller:

```bash
uv run chess-gantry --config config.json web
```

Use `--no-browser` for headless startup. The server binds to localhost by
default. A network-visible bind requires explicit network permission.

## Troubleshooting

### No `/dev/ttyUSB0`

1. Restore controller power.
2. Reconnect USB.
3. Close Cura, Pronterface, Arduino tools, or other serial clients.
4. Run `uv run chess-gantry --config config.json ports`.
5. Run `uv run chess-gantry --config config.json diagnose`.

### Permission Denied

Ensure the current user can access the serial device, commonly through the
`dialout` group, then log out and back in after changing group membership.

### Controller Disconnects When Magnet Turns On

Treat this as an electrical load or interference problem. Switch both outputs
off, power-cycle the controller, and correct the magnet driver circuit. Do not
solve a controller reset by increasing pulse duration or repeatedly retrying
full power.

### LCD Still Shows Fan 0

Connector labels and Marlin logical indices differ across Ender boards and
firmware. This project currently sends full PWM to both `P0` and `P1`. Verify
the actual electrical output with a meter and the board schematic rather than
relying only on the LCD label.

### Pending Transaction Error

Run `reconcile`, inspect the stored transaction, physically inspect the board,
and then explicitly mark it applied or discard it.

## Current Verification

The latest completed verification included:

- 77 automated tests passing
- Python compilation passing
- Black and Prettier checks passing
- repository policy checks passing
- exact presentation G-code ordering tests passing
- simulated continuous-power presentation streaming passing
- dual `P0` and `P1` fan command tests passing
- JSON restart persistence passing
- public Lichess polling and PGN planning passing
- browser demo API startup passing

Physical electromagnet reliability is not software-verified because the direct
load caused a controller or USB reset. Resolve that electrical issue before
claiming a fully validated physical magnet demo.

Additional direct-command details are available in [RUNNING.md](RUNNING.md).
