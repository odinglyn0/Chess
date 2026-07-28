<h1 align="center">Chess Gantry</h1>

<p align="center">
  A collision-aware control system for a physical, self-moving chessboard.
</p>

<table align="center">
  <tr>
    <td bgcolor="#000000">
      <img src="./FullLogoWhite.webp" alt="Patch" width="190">
    </td>
    <td>
      <strong>A Patch project by</strong><br>
      Basil Amin · Ben Hewston · Kelvin Gao · Odin Glynn
    </td>
  </tr>
</table>

Chess Gantry turns legal chess moves into safe Marlin G-code for a magnetic
Cartesian gantry. It plans routes around occupied squares, moves pieces,
mirrors public Lichess games, and keeps recoverable local state if a physical
move is interrupted.

Current calibrated geometry:

```text
Inner gantry width: 330 mm
Outer gantry height: 300 mm
Chess grid: 300 x 300 mm
Software square size: 37.5 x 37.5 mm
```

The physical squares were described as 4 cm, but eight exact 40 mm squares need
320 mm of height. Because the selected safe travel height is 300 mm, software
uses 37.5 mm square centers so all eight ranks remain reachable. No firmware
reflash is required; host homing remaps to `X2 Y298 Z328`.

## What it does

- Plans collision-aware piece paths with A*
- Supports moves, captures, en passant, and ordered Lichess castling transfers
- Rejects promotion until the required physical piece replacement is handled
- Streams guarded movement and magnet commands to Marlin over serial
- Tracks board state, pending moves, and an append-only audit log locally
- Follows public Lichess games in real time
- Includes a browser controller, raw G-code debug console, and hardware tests
- Runs entirely without Redis, a database server, or cloud state

## Quick start

Requires Python 3.9+ and [`uv`](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/odinglyn0/Chess.git
cd Chess
./scripts/install_pi.sh
```

Plan the included `e2e4` move without touching hardware:

```bash
uv run chess-gantry --config config.json \
  plan examples/move_e2_e4.json --summary-json
```

Launch the complete simulated browser experience:

```bash
./scripts/live_demo.sh
```

Then open <http://127.0.0.1:8000>.

## Using the gantry

> [!WARNING]
> The gantry and electromagnet can cause injury, overheating, controller resets,
> or hardware damage. Keep an independent emergency cutoff within reach. Clear
> every travel path, verify wiring and current limits, and never leave an
> energized electromagnet unattended.

Before the first physical move, calibrate `config.json`, set
`safety.calibrated` to `true`, and work through the commissioning checklist in
[RUNNING.md](./RUNNING.md).

Daily startup:

```bash
uv run chess-gantry --config config.json ports
uv run chess-gantry --config config.json diagnose
uv run chess-gantry --config config.json home-gantry \
  --record data/gantry_home.json \
  --confirm-motion --confirm-clear-path
```

Execute a move only after inspecting its dry-run:

```bash
uv run chess-gantry --config config.json \
  execute examples/move_e2_e4.json --confirm-motion
```

For a physical browser controller:

```bash
uv run chess-gantry --config config.json web
```

For authenticated access from other devices on the same trusted LAN:

```bash
./scripts/run_network_ui.sh
```

Open the complete token URL printed by the launcher. All commands and serial
access still run on the gantry computer.

After connecting and homing in the UI, enable **arrow-key motion** to jog the
gantry. Left/Right move the inner gantry, Up/Down move the paired outer gantry,
and Escape disarms keyboard motion. The live coordinate panel polls Marlin
`M114` and displays raw outer X/Y and inner Z positions in real time.

The checked-in firmware image targets only a Creality 4.2.2 board with an
STM32F103RET6 MCU. Verify the board and follow the exact flashing procedure in
[RUNNING.md](./RUNNING.md) before using it.

## How it works

```text
Move JSON / Lichess
        │
        ▼
 legality + board-state validation
        │
        ▼
 collision-aware route planning
        │
        ▼
 bounded Marlin G-code
        │
        ▼
 serial acknowledgements ──► committed JSON state
              │
              └─────────────► recovery journal on interruption
```

Schemas and examples live in [`schemas/`](./schemas) and
[`examples/`](./examples). Runtime state is stored under `data/` by default:

| File                | Purpose                                |
| ------------------- | -------------------------------------- |
| `board_state.json`  | Last committed physical board position |
| `pending_move.json` | Interrupted or unconfirmed move        |
| `audit.jsonl`       | Append-only operational history        |

If execution stops mid-move, inspect the journal before doing anything else:

```bash
uv run chess-gantry --config config.json reconcile
```

## Development

Install the Python and formatting dependencies:

```bash
uv sync
npm ci
```

Run the full software checks:

```bash
./scripts/check.sh
npm run check
./scripts/demo_check.sh
```

`demo_check.sh` exercises the complete simulated workflow and never opens the
physical serial port.

## Documentation

- [Running and commissioning](./RUNNING.md) — installation, calibration,
  hardware checks, recovery, and troubleshooting
- [Lichess pipeline](./LICHESS_PIPELINE.md) — replay and live-follow workflow
- [Integration notes](./INTEGRATION_NOTES.md) — hardware/software boundaries
- [`config.example.json`](./config.example.json) — documented configuration
- [`uv run chess-gantry --help`](./src/chess_gantry/cli.py) — complete CLI

Built for a chessboard that does more than wait for the next move.
