# Lichess To Gantry Pipeline

The gantry follows a public Lichess game directly through
[`berserk`](https://github.com/lichess-org/berserk), the official Lichess API
client. There is no separate stream service, container, or Git submodule: the
gantry host talks to `https://lichess.org` over HTTPS, receives moves in real
time, and drives Marlin over its own serial connection.

Each move is parsed with [`python-chess`](https://python-chess.readthedocs.io/),
translated into the gantry's native move JSON with stable piece identifiers,
validated against the persistent board state, and turned into Marlin G-code.
Lichess delays its public live-game stream by a few plies to discourage
cheating, so the physical board trails the online game by that margin.

## Authentication

Watching public games needs no credentials. To raise rate limits or read your
own games, export a Lichess personal API token as `LICHESS_TOKEN`; the client
picks it up automatically.

```bash
export LICHESS_TOKEN="lip_xxxxxxxxxxxxxxxx"
```

## Replay a game's currently recorded moves

To dry-run every move currently present in the public PGN export without moving
hardware or changing persistent board state:

```bash
uv run chess-gantry --config config.json --state data/board_state.json \
  lichess-pgn GAME_ID --output-dir data/lichess
```

## Follow a live game in real time

`lichess-follow` opens the Lichess move stream and reacts as each new ply
arrives. It writes per-move JSON and a G-code plan once, prints every generated
program, and reconnects automatically if the stream drops. A session file in
the output directory remembers emitted moves; use `--reset-session` only to
deliberately regenerate all files from the saved initial board state.

```bash
uv run chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID --output-dir data/lichess
```

For a one-shot catch-up on the current game state, add `--once`. The
`--interval` value is the delay before reconnecting a dropped stream.

Hardware streaming is opt-in and requires both acknowledgements below. Moves
already recorded as dry runs in the session are never sent unless
`--execute-existing` is also specified:

```bash
uv run chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID --execute --confirm-motion --execute-existing
```

Only execute after the physical board, serial connection, homing, board
dimensions, and planned path have all been verified. Each successful ply commits
the new board state; a failure leaves a recovery journal and stops progress
until the operator reconciles the real board. The CLI refuses to plan or execute
while `data/pending_move.json` exists.

If a dry-run position is too dense for the configured A* keep-out, test a
different value without changing `config.json` or allowing hardware execution:

```bash
uv run chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID --obstacle-keepout-mm 11 --once
```

This is a geometric simulation aid only. Do not lower the hardware configuration
until the physical piece sizes, magnet clearance, and critical path are measured.

## Fixed motor test

Before a chess move, test the mechanism with a fixed, guarded movement on each
mechanical group. It forces the magnet off, waits for every motion to finish,
then disables stepper motors using `M84`. It does not touch board state or
create a pending chess transaction.

First print and inspect the serial-free outer X/Y and inner E G-code:

```bash
uv run chess-gantry --config config.json motor-test
```

An optional in-memory transport check is available with
`motor-test --confirm-motion --demo` and still opens no serial port.

After checking endstops, workspace clearance, serial diagnostics, and the
physical travel limits, send the same fixed program to Marlin:

```bash
uv run chess-gantry --config config.json motor-test --confirm-motion
```

The real command prints the exact transmitted G-code after every Marlin command
has acknowledged. It requires `safety.calibrated: true`. It uses `M82`,
`M302 P1`, and `G92` to define the E motor as the absolute second outer axis,
issues no `G28`, and restores cold-extrusion protection with `M302 P0`.

With the gantry manually placed and squared at a safe starting position, the
motor test uses `M82`, `M302 P1`, and `G92 X0 Y350 E350` to define the E motor as
the absolute second outer axis. It issues no `G28`, restores cold-extrusion
protection with `M302 P0`, and does not call the homing workflow.

## Supported upstream events

Normal moves, ordinary captures, and en passant translate directly. Castling
and promotion are rejected rather than moving pieces incorrectly: castling
needs a king and rook transfer, while promotion needs a verified physical
piece-replacement mechanism.
