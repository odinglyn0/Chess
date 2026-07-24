# Chess Gantry

Chess Gantry converts chess moves into collision-aware Marlin G-code for a
magnetic Cartesian gantry. It stores board state, recovery transactions, audit
history, Lichess sessions, move JSON, and generated G-code in ordinary local
files. No database or external state service is required.

## Demo Quick Start

Install once:

```bash
uv sync
npm ci
```

Run all tests, checks, move planning, electromagnet simulation, and the
64-square board sweep simulation:

```bash
./scripts/demo_check.sh
```

Launch the simulated browser controller:

```bash
./scripts/live_demo.sh
```

Open <http://127.0.0.1:8000>. Neither command opens a physical serial port.

## Your Lichess Game

The configured demo game is:

```text
6RkOwfp1
```

All files for it live under:

```text
data/lichess/6RkOwfp1/
```

Run a network and planning check against its current public PGN:

```bash
./scripts/lichess_game.sh check
```

Follow it in real time without hardware:

```bash
./scripts/lichess_game.sh dry-run
```

Stop with `Ctrl+C`.

After physical calibration and the complete hardware test ladder, place every
piece in the standard starting position, reset JSON state, then follow and move
in real time:

```bash
./scripts/lichess_game.sh reset
./scripts/lichess_game.sh play
```

The follower polls every two seconds. It mirrors both players' moves, supports
normal moves, captures, en passant, and castling, and commits
`board_state.json` only after Marlin acknowledges the entire movement. Promotion
is rejected because physical piece replacement is not implemented.

Use a different public Lichess game ID as the second argument:

```bash
./scripts/lichess_game.sh dry-run OTHER_GAME_ID
./scripts/lichess_game.sh play OTHER_GAME_ID
```

The program observes a public Lichess game. It does not create games, submit
moves, press a clock, or control a Lichess account.

## JSON State

The normal local defaults are:

```text
data/board_state.json
data/pending_move.json
data/audit.jsonl
```

The Lichess helper gives each game its own directory containing:

```text
board_state.json
pending_move.json
audit.jsonl
dry-run.session.json
physical.session.json
dry-run/*.json and *.gcode
physical/*.json and *.gcode
```

Writes are atomic and protected by local file locks. A failed physical move
leaves the pending journal in place so later moves cannot silently corrupt
state.

Show the state for game `6RkOwfp1`:

```bash
./scripts/lichess_game.sh status
```

Reset only after physically restoring the standard position:

```bash
./scripts/lichess_game.sh reset
```

Inspect an interrupted move:

```bash
./scripts/lichess_game.sh reconcile
```

After checking the physical board, use the direct command from
[RUNNING.md](RUNNING.md) to mark the transaction applied or discard it.

## Physical Calibration Required

> [!WARNING]
> Moving hardware and electromagnets can cause injury, overheating, or machine
> damage. Keep an independent emergency cutoff available. A configuration value
> of `safety.calibrated: true` is only an operator assertion.

The panel is 500 x 600 mm, but that does not define safe tool-center travel.
The checked-in physical `config.json` still contains an unusable
`square_size_mm: 0.05`. Before any physical board sweep or chess move, measure
and set:

- usable X and Y tool-center minimums and maximums
- center of `a1` and actual square pitch
- axis flips and swap behavior
- safe park position
- capture-slot coordinates
- coordinate-origin commands and feed limits

`config.demo.json` is a simulated 500 x 600 workspace. Do not treat its
coordinates as physical measurements.

## Hardware Test Ladder

Run in this order after entering measured geometry.

Read-only controller checks:

```bash
uv run chess-gantry --config config.json ports
uv run chess-gantry --config config.json diagnose
```

Print a 5 mm, 300 mm/min test without connecting:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 5 --feed-mm-min 300
```

Run it physically:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 5 --feed-mm-min 300 --confirm-motion
```

Print a fixed 20 mm movement test at 1,200 mm/min with the configured fan outputs energized during
each movement leg:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 20 --feed-mm-min 1200 --magnet-on
```

Run that exact sequence physically only after inspecting the printed G-code:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 20 --feed-mm-min 1200 --magnet-on \
  --confirm-motion --confirm-magnet
```

For a presentation-only continuous hold, repeat the 20 mm four-leg path three
times. Both configured fan outputs stay at full PWM until all movement ends:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 20 --feed-mm-min 1200 --magnet-on \
  --presentation-loops 3 --confirm-motion --confirm-magnet
```

The command refreshes both `M106 ... S255` outputs before every movement leg
and sends no `M107` until the final return. Presentation mode rejects sequences
whose estimated energized movement exceeds 30 seconds.

Test the Ender 3 Pro electromagnet output for one second:

```bash
uv run chess-gantry --config config.json magnet-test --duration-s 1
uv run chess-gantry --config config.json magnet-test \
  --duration-s 1 --confirm-motion
```

The configuration currently drives both logical fan indices with `M106 P0 S255`
and `M106 P1 S255`, then disables both with `M107 P0` and `M107 P1`. On the
connected controller, energizing the directly attached electromagnet caused a
USB/controller reset. Do not retry under load until the magnet is connected
through a correctly rated MOSFET or relay driver with flyback protection and an
appropriate power supply.

Generate the faster 64-square sweep without connecting:

```bash
uv run chess-gantry --config config.json board-sweep \
  --feed-mm-min 1800 --magnet-on \
  --output data/board-sweep.gcode
```

After inspecting that file, remove all pieces and obstructions, place the
gantry at the configured origin, and run:

```bash
uv run chess-gantry --config config.json board-sweep \
  --feed-mm-min 1800 --magnet-on \
  --confirm-motion --confirm-empty-board \
  --confirm-origin --confirm-magnet
```

The sweep visits all 64 square centers in serpentine order and pulses the configured output for
300 ms at each center, with the magnet off during travel.

## Tests

```bash
./scripts/check.sh
npm run check
```

See [RUNNING.md](RUNNING.md) for direct commands, JSON paths, reset/recovery,
and troubleshooting details.
