<p align="center">
  <img src="./FullLogoWhite.webp" alt="Patch" width="220">
</p>

<h1 align="center">Chess Gantry</h1>

<p align="center">
  <strong>A physical chessboard that moves the pieces.</strong><br>
  Collision-aware planning, Marlin motion control, live Lichess games, and a secure browser dashboard.
</p>

<p align="center">
  <img alt="Python 3.9+" src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white">
  <img alt="Raspberry Pi 3B+" src="https://img.shields.io/badge/Raspberry%20Pi-3B%2B-C51A4A?logo=raspberrypi&logoColor=white">
  <img alt="Marlin" src="https://img.shields.io/badge/Firmware-Marlin-008080">
  <img alt="Distroless" src="https://img.shields.io/badge/Runtime-Distroless-2496ED?logo=docker&logoColor=white">
</p>

<p align="center">
  A <strong>Patch</strong> project by<br>
  <strong>Basil Amin · Ben Hewston · Kelvin Gao · Odin Glynn</strong>
</p>

---

## What It Does

Chess Gantry translates legal chess moves into guarded G-code for a magnetic Cartesian gantry. It can:

- home three independently driven axes against physical endstops;
- move pieces between measured 40 mm square centers;
- plan collision-aware routes around occupied squares;
- control an electromagnet through Marlin fan output `P0`;
- mirror fresh public Lichess games using streaming move updates;
- provide authenticated local and network browser controls;
- recover interrupted physical moves from local JSON state.

No Redis, cloud database, or desktop environment is required.

## The Machine

| Property | Value |
| --- | --- |
| Inner gantry width | 330 mm |
| Outer paired gantry height | 300 mm |
| Chessboard | 8 x 8 |
| Square-center spacing | 40 mm |
| Nearest-home square | **h1** |
| Nearest-home center | `X2 Y298 Z320` |
| Homed host reference | `X2 Y298 Z328` |

### Motor Mapping

```text
Physical X driver -> logical X -> x_min
Physical Y driver -> logical Y -> y_max
Physical E driver -> logical Z -> z_max
Physical Z driver -> unused
Electromagnet     -> fan P0
```

The physical E connector is intentionally controlled as logical Marlin Z. The host homes with `G28 X Y Z`, waits for completion, and applies the measured coordinate remap:

```gcode
G28 X Y Z
M400
G92 X2 Y298 Z328
M400
```

### Measured Board Centers

The four measured raw Marlin corner centers are:

```text
h1: X2   Y298 Z320
a1: X2   Y298 Z40
h8: X282 Y18  Z320
a8: X282 Y18  Z40
```

The center spacing is exactly 40 mm. Seven intervals separate eight centers, so the traversal spans 280 mm in each board direction.

> [!IMPORTANT]
> Physical capture slots are currently disabled. The measured 40 mm grid leaves insufficient safe off-board storage inside the 330 mm travel width. Normal moves and non-capturing demonstrations work. Captures require a separately measured external storage area.

## Browser Control

Run locally:

```bash
uv run chess-gantry --config config.json web
```

Open <http://127.0.0.1:8000>.

The dashboard includes:

- live raw Marlin X/Y/Z coordinates;
- guarded arrow-key jogging;
- homing, movement, magnet, circle, perimeter, and 64-square tests;
- board state, reset, audit, and recovery tools;
- immediate live Lichess TV mode;
- task logs, cancellation, and emergency stop.

### Authenticated LAN Access

```bash
./scripts/run_network_ui.sh
```

Open the complete token URL printed by the server from another device on the same trusted network. Commands and serial access remain on the gantry computer.

Do not expose the plain-HTTP dashboard directly to the internet.

## Raspberry Pi 3B+

The recommended deployment is Raspberry Pi OS Lite 64-bit with Docker. The Pi host does not need `uv`, Node.js, or a Python virtual environment.

```bash
sudo apt update
sudo apt install -y git curl
git clone --recurse-submodules https://github.com/odinglyn0/Chess.git
cd Chess
./scripts/install_pi.sh
```

The installer configures Docker, serial access, persistent state, a random dashboard token, and the web service.

### Container Architecture

```text
Build stage: Fedora 42
Runtime: scratch-based distroless root filesystem
Platform: linux/arm64
```

The production image contains Python, the application, runtime dependencies, and a small `uv run` compatibility shim. It contains no shell, package manager, Git client, Node.js, or compiler.

Manage the Pi service with:

```bash
./scripts/pi_docker.sh status
./scripts/pi_docker.sh logs
./scripts/pi_docker.sh restart
./scripts/pi_docker.sh firmware-check
./scripts/pi_docker.sh test
```

### Deploy Future Changes

After changes are pushed, update the Pi with one command:

```bash
cd ~/Chess
./scripts/pi_docker.sh update
```

This performs a fast-forward pull, updates submodules, rebuilds the image, and recreates the distroless runtime. `data/`, `config.json`, and `.env.docker` are preserved.

## 64-Square Center Test

The primary calibration test homes the gantry, approaches h1, and visits every square center in a serpentine path. Every adjacent move is exactly 40 mm.

Simulate it:

```bash
uv run chess-gantry --config config.demo.json square-center-demo \
  --feed-mm-min 1800 --dwell-ms 150 --confirm-motion --demo
```

Run physically with the magnet off:

```bash
uv run chess-gantry --config config.json square-center-demo \
  --feed-mm-min 1800 --dwell-ms 150 \
  --confirm-motion --confirm-clear-workspace
```

Run with continuous magnet power:

```bash
uv run chess-gantry --config config.json square-center-demo \
  --feed-mm-min 1800 --dwell-ms 150 --magnet-on \
  --confirm-motion --confirm-clear-workspace --confirm-magnet
```

## Live Lichess Demo

The dashboard can follow a new public Lichess game with low latency through Lichess's streaming game API.

1. Create a fresh standard Lichess game with zero moves.
2. Reset the physical board to its starting position.
3. Start the authenticated dashboard.
4. Enter the game ID in **Live Lichess TV game**.
5. Confirm the board and motion checks.
6. Press **Start immediate live play** before White's first move.

Each web-server session creates fresh isolated board state, homes once, and executes newly streamed plies through one persistent serial connection.

> [!WARNING]
> The live follower stops safely at captures while physical capture storage is disabled. Promotion also requires physical piece replacement.

## State And Recovery

```text
data/board_state.json   Last committed physical board state
data/pending_move.json  Interrupted move recovery journal
data/audit.jsonl        Append-only operation history
```

Inspect a pending move:

```bash
uv run chess-gantry --config config.json reconcile
```

Emergency stop:

```bash
uv run chess-gantry --config config.json stop
```

Reset or power-cycle Marlin and home again after `M112`.

## Development

```bash
uv sync
npm ci
./scripts/check.sh
npm run check
```

The automated suite covers geometry, planning, persistence, serial protocol, firmware configuration, container deployment, authentication, dashboard task ownership, keyboard jogging, and live Lichess state.

## Safety

> [!WARNING]
> This system moves real hardware and energizes an electromagnet. Keep an independent physical cutoff within reach, clear every requested path, verify electrical flyback protection, and never leave the magnet energized unattended. Software checks do not replace safe mechanical and electrical design.

## Documentation

- [RUNNING.md](./RUNNING.md) - commissioning, commands, and recovery
- [DOCKER.md](./DOCKER.md) - container build and deployment
- [LICHESS_PIPELINE.md](./LICHESS_PIPELINE.md) - Lichess integration
- [INTEGRATION_NOTES.md](./INTEGRATION_NOTES.md) - system boundaries
- [config.example.json](./config.example.json) - complete configuration

---

<p align="center">
  <strong>Built at Patch for a chessboard that refuses to sit still.</strong>
</p>
