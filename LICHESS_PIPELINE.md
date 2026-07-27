# Lichess To Gantry Pipeline

This repository pins `https://github.com/odinglyn0/Chess` as the
`services/lichess_stream` Git submodule. Its FastAPI service reads Lichess's
public NDJSON game stream and emits WebSocket move envelopes with stable piece
identifiers. The gantry converts each `type: "move"` envelope into its native
move JSON, validates it against `data/board_state.json`, and produces Marlin
G-code.

## Start the services

Initialize the upstream service after cloning this repository:

```bash
git submodule update --init --recursive
```

Start the upstream Lichess WebSocket API on port 8010. This is deliberately
separate from the local gantry UI, which uses port 8000.

```bash
./scripts/start_lichess_stream.sh
```

The API is then available at `ws://127.0.0.1:8010/ws/GAME_ID` and
`http://127.0.0.1:8010/games/GAME_ID/state`.

## Convert an API event safely

Save exactly one `type: "move"` WebSocket message from the upstream service,
then produce both native move JSON and G-code without moving the gantry:

```bash
.venv/bin/chess-gantry --config config.json --state data/board_state.json \
  lichess-event examples/lichess_e2_e4_event.json \
  --move-output data/lichess_e2e4.json \
  --gcode-output data/lichess_e2e4.gcode
```

The generated JSON can be inspected and planned again with the normal CLI.
Physical execution is intentionally a separate, explicit operation:

```bash
.venv/bin/chess-gantry --config config.json --state data/board_state.json \
  execute data/lichess_e2e4.json --confirm-motion
```

Only execute after the upstream state, physical board, serial connection,
homing, board dimensions, and planned path have all been verified. The CLI
refuses to plan or execute if `data/pending_move.json` exists; reconcile that
journal after inspecting the real board.

## Follow a live game

After starting the Lichess service, this subscribes continuously and writes
each received upstream event as native gantry JSON plus a G-code plan:

```bash
.venv/bin/chess-gantry --config config.json --state data/board_state.json \
  lichess-watch GAME_ID --output-dir data/lichess
```

Planning does not update board state, so it is appropriate for inspecting the
first queued move only. For a physically synchronized board, execute every
received move only after diagnosis, homing, and physical confirmation:

```bash
.venv/bin/chess-gantry --config config.json --state data/board_state.json \
  lichess-watch GAME_ID --execute --confirm-motion --output-dir data/lichess
```

## Replay a live game's currently recorded moves

Lichess delays its public live-game stream. To immediately dry-run every move
currently present in the public PGN export, use:

```bash
.venv/bin/chess-gantry --config config.json --state data/board_state.json \
  lichess-pgn GAME_ID --output-dir data/lichess
```

This never moves hardware or writes the persistent board state.

## Automatically create files for new moves

This polls the public PGN every five seconds, creates per-move JSON and G-code
files only once, and prints every generated G-code program to the terminal:

```bash
.venv/bin/chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID --output-dir data/lichess
```

For an immediate one-shot check, add `--once`. A session file in the output
directory remembers emitted moves; use `--reset-session` only to deliberately
regenerate all files from the saved initial board state.

Hardware streaming is opt-in and requires both acknowledgements below. Existing
dry-run moves are never sent unless `--execute-existing` is also specified:

```bash
.venv/bin/chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID --execute --confirm-motion --execute-existing
```

If a dry-run position is too dense for the configured A* keep-out, test a
different value without changing `config.json` or allowing hardware execution:

```bash
.venv/bin/chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID --obstacle-keepout-mm 11 --once
```

This is a geometric simulation aid only. Do not lower the hardware configuration
until the physical piece sizes, magnet clearance, and critical path are measured.

## Fixed motor test

Before a chess move, test the mechanism with a fixed, guarded 50 mm movement on each mechanical group.
It homes first, forces the magnet off, waits for every motion to finish, then
disables stepper motors using `M84`. It does not touch board state or create a
pending chess transaction.

First print and inspect the serial-free outer X/Y and inner E G-code:

```bash
.venv/bin/chess-gantry --config config.json motor-test
```

Every outer-axis move uses mirrored X/Y targets whose sum is 170, such as
`G1 X75 Y95 F4242`. Inner movement uses E independently, such as
`G1 E75 F3000`. An optional in-memory transport check is available with
`motor-test --confirm-motion --demo` and still opens no serial port.

After checking endstops, workspace clearance, serial diagnostics, and the
physical travel limits, send the same fixed program to Marlin:

```bash
.venv/bin/chess-gantry --config config.json motor-test --confirm-motion
```

The real command prints the exact transmitted G-code after every Marlin command
has acknowledged. It requires `safety.calibrated: true` and rejects a workspace
that does not include 200 mm of inner E travel and 200 mm of mirrored outer X/Y
travel in both directions.

With the gantry manually placed and squared at a safe starting position, the
motor test uses `M82`, `M302 P1`, and `G92 X350 Y0 E0` to define the E motor as
the absolute second outer axis. It issues no `G28`, restores cold-extrusion
protection with `M302 P0`, and does not call the homing workflow.

## Supported upstream events

Normal moves, ordinary captures, and en passant translate directly. Castling
and promotion are rejected rather than moving pieces incorrectly: castling
needs a king and rook transfer, while promotion needs a verified physical
piece-replacement mechanism.
