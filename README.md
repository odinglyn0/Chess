<h1 align="center">Chess Gantry</h1>

<p align="center">
  A collision-aware control system for a physical, self-moving chessboard.
</p>

<table align="center">
  <tr>
    <td bgcolor="#000000">
      <img src="./FullLogoWhite.webp" alt="Chess Gantry" width="190">
    </td>
    <td>
      <strong>A Patch project by</strong><br>
      Basil Amin · Ben Hewston · Kelvin Gao · Odin Glynn
    </td>
  </tr>
</table>

Chess Gantry converts chess moves into guarded Marlin G-code for a magnetic
Cartesian gantry. It handles homing, measured square centers, route planning,
electromagnet control, JSON state recovery, live Lichess following, and an
authenticated browser operations dashboard.

## Highlights

- Measured 8 x 8 grid with exact 40 mm center-to-center spacing
- Firmware X/Y alignment against independent endstops
- Physical E-driver connector mapped by Marlin as logical Z
- Collision-aware A* movement planning around occupied squares
- Local JSON state with crash-recovery journal and audit log
- Browser keyboard jogging with live `M114` X/Y/Z coordinates
- Authenticated LAN dashboard for tests, demos, and physical operations
- 64-square center traversal with optional continuous magnet power
- Public Lichess replay and near-real-time physical following
- No Redis or external state server required

## Measured Geometry

The machine envelope is:

```text
Inner gantry / logical Z width: 330 mm
Outer paired X/Y height:       300 mm
```

The measured square-center geometry is:

```text
Square spacing: 40 mm
Logical center range: inner 40..320 mm, outer 18..298 mm
```

Measured raw Marlin corner centers:

```text
Nearest home: X2   Y298 Z320
Corner 2:     X282 Y18  Z320
Corner 3:     X282 Y18  Z40
Corner 4:     X2   Y298 Z40
```

These define eight centers per axis because seven intervals separate eight
squares:

```text
7 intervals x 40 mm = 280 mm
```

The software board geometry is therefore:

```json
{
  "square_size_mm": 40.0,
  "origin_x_mm": 40.0,
  "origin_y_mm": 18.0
}
```

The physical square edges may extend beyond the reachable center envelope. The
gantry operates on measured centers, not outer board edges.

> [!IMPORTANT]
> Capture slots are currently disabled. A 40 mm grid from inner center 30 to
> 320 leaves only 10 mm on the far side inside the 330 mm travel width, which is not
> enough for safe off-board piece storage. Normal moves, calibration traversals,
> and non-capturing game demonstrations work. Physical captures require a
> measured external capture area or a larger travel envelope.

## Hardware Mapping

```text
Physical X driver -> logical X -> x_min
Physical Y driver -> logical Y -> y_max
Physical E driver -> logical Z -> z_max
Physical Z driver -> unused
Magnet output     -> fan P0
```

The installed custom Marlin firmware homes with `G28 X Y Z`. The host then
remaps the backed-off native home into the measured envelope:

```gcode
G28 X Y Z
M400
G92 X2 Y298 Z328
M400
```

No firmware reflash is required for the measured 330 x 300 mm host envelope;
the installed native 350 mm firmware limits safely contain it.

## Safety

> [!WARNING]
> The gantry and electromagnet can injure people, damage hardware, overheat, or
> lose serial communication. Keep an independent physical power cutoff within
> reach. Clear every requested path. Never leave the magnet energized
> unattended. Do not expose the control UI directly to the internet.

Physical operations use explicit confirmation gates, one-task-at-a-time serial
ownership, bounded coordinates, and best-effort magnet/motor shutdown. These
controls do not replace a physical cutoff or correct electrical protection.

## Install

Requires Python 3.9+, [`uv`](https://docs.astral.sh/uv/), and Node.js.

```bash
git clone --recurse-submodules https://github.com/odinglyn0/Chess.git
cd Chess
uv sync
npm ci
```

Verify everything without opening the physical serial port:

```bash
./scripts/check.sh
npm run check
./scripts/demo_check.sh
```

## Raspberry Pi 3B+ Deployment

Chess Gantry supports a Raspberry Pi 3 Model B+ running Raspberry Pi OS Lite.
Use **Raspberry Pi OS Lite 64-bit** when possible. The Pi 3B+ has a 64-bit Arm
Cortex-A53 processor, and the 64-bit image avoids mixed ARMv7/aarch64 package
resolution issues.

The normal runtime is lightweight:

- Python 3.9 or newer
- `pyserial`, `python-chess`, and `berserk`
- local JSON/JSONL persistence
- USB serial communication with Marlin
- built-in HTTP operations dashboard
- no Redis, database server, desktop environment, or Docker requirement

Node.js is only required for `npm run check`, Prettier, and dashboard operations
that run repository quality checks. Normal movement, Lichess following, and the
web server do not depend on Node.js at runtime.

### Install Raspberry Pi Packages

On Raspberry Pi OS Lite:

```bash
sudo apt update
sudo apt install -y \
  git \
  curl \
  python3 \
  python3-venv \
  nodejs \
  npm
```

Install `uv` using its official standalone installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
```

Verify the toolchain:

```bash
uv --version
python3 --version
node --version
npm --version
```

Clone and install the project:

```bash
git clone --recurse-submodules https://github.com/odinglyn0/Chess.git
cd Chess
uv sync
npm ci
./scripts/install_pi.sh
```

### Serial Permissions

Add the current Pi user to the serial-port group:

```bash
sudo usermod -aG dialout "$USER"
sudo reboot
```

After reboot:

```bash
cd ~/Chess
uv run chess-gantry --config config.json ports
uv run chess-gantry --config config.json diagnose
```

### Headless Network UI

Raspberry Pi OS Lite has no local desktop or browser. Start the authenticated
LAN interface on the Pi:

```bash
cd ~/Chess
./scripts/run_network_ui.sh
```

Open the complete token URL printed by the launcher from a phone, tablet, or
computer on the same trusted network:

```text
http://192.168.1.50:8000/?token=LONG_RANDOM_TOKEN
```

All serial commands continue to run on the Pi. The remote browser does not
access `/dev/ttyUSB0` directly.

For localhost-only headless startup:

```bash
uv run chess-gantry --config config.json web --no-browser
```

### Tests On The Pi

Runtime test suite:

```bash
./scripts/check.sh
```

Formatting, policy, and Git hygiene checks:

```bash
npm run check
```

Complete simulated readiness workflow:

```bash
./scripts/demo_check.sh
```

The Pi 3B+ can run the complete suite, but installation and formatting checks
will be slower than on a desktop. Normal serial control, position polling,
planning, Lichess following, and the browser dashboard are substantially
lighter.

Build Marlin firmware on a faster desktop when practical. The Pi only needs the
host software after the Ender controller has been flashed.

### Pi Power And Networking

Use a stable dedicated Raspberry Pi supply rated for approximately 5 V at 2.5 A
or better. Do not rely on the Ender controller's USB connection to power the Pi.
A separate stable supply reduces USB serial disconnects during motor and magnet
operation.

Ethernet is preferred for the remote operations dashboard, although Wi-Fi is
supported. Do not expose the plain-HTTP control interface directly to the
internet.

Recommended deployment:

```text
Raspberry Pi 3B+
Raspberry Pi OS Lite 64-bit
Stable dedicated 5 V supply
USB connection to the Ender controller
Ethernet where available
Dashboard opened from another trusted LAN device
```

## Browser Dashboard

Start local physical control:

```bash
uv run chess-gantry --config config.json web
```

Open <http://127.0.0.1:8000>.

Start a safe simulated dashboard:

```bash
uv run chess-gantry --config config.demo.json web --demo
```

Physical operation cards are disabled by the server in demo mode.

### Authenticated LAN Access

```bash
./scripts/run_network_ui.sh
```

Open the complete token URL printed by the launcher from another device on the
same trusted LAN. Commands and `/dev/ttyUSB0` access remain on the gantry
computer. Missing or incorrect tokens receive HTTP 401.

The dashboard includes:

- firmware and endstop checks
- homing and movement tests
- magnet pulse, circle, perimeter, and workspace demos
- measured 64-square center traversal
- board JSON state and recovery operations
- Lichess check, dry run, and physical play
- live task output and task cancellation

### Keyboard Jogging

After connecting and homing, check **Enable arrow-key motion**.

```text
Left / Right -> inner gantry width
Up / Down    -> paired outer gantry height
Escape       -> disarm keyboard motion
```

Select a 0.5, 1, 5, or 10 mm step and a feed rate. Keyboard movement is ignored
while typing, while disconnected/unhomed, during key repeat, or while another
dashboard task owns serial. The live position panel polls `M114` and displays
raw outer X, outer Y, and inner Z coordinates.

## 64-Square Center Test

This is the primary measured-board calibration test. It:

1. Homes X/Y/Z.
2. Applies the measured home remap.
3. Approaches the corrected nearest-home center at `X2 Y298 Z320`.
4. Visits all 64 unique centers in a serpentine path.
5. Moves exactly 40 mm between every adjacent center.
6. Optionally keeps the electromagnet on continuously.
7. Switches the magnet off, returns home, and disables motors.

There is one 40 mm move per adjacent square center. Each row has seven such
moves, followed by one 40 mm move to the next row. After the initial approach,
the complete traversal contains 63 square-to-square moves.

### Generate G-code

```bash
uv run chess-gantry --config config.json square-center-demo \
  --feed-mm-min 1800 \
  --dwell-ms 150 \
  --output data/square-centers.gcode
```

### Simulate

```bash
uv run chess-gantry --config config.demo.json square-center-demo \
  --feed-mm-min 1800 \
  --dwell-ms 150 \
  --confirm-motion \
  --demo
```

### Physical Test, Magnet Off

Clear the complete board path and keep the emergency cutoff ready:

```bash
uv run chess-gantry --config config.json square-center-demo \
  --feed-mm-min 1800 \
  --dwell-ms 150 \
  --confirm-motion \
  --confirm-clear-workspace
```

### Physical Test, Magnet Continuously On

```bash
uv run chess-gantry --config config.json square-center-demo \
  --feed-mm-min 1800 \
  --dwell-ms 150 \
  --magnet-on \
  --confirm-motion \
  --confirm-clear-workspace \
  --confirm-magnet
```

At 1800 mm/min with 150 ms dwell per center, the continuous magnet interval is
approximately 94 seconds. The command rejects estimates above 120 seconds. The
driver, supply, coil, and cooling must safely support this duty cycle.

In the browser dashboard use:

- **Simulate all 64 square centers**
- **Visit all 64 square centers**
- **Visit 64 centers with magnet on**

The magnet-on card requires both clear-workspace and magnet-safety confirmations.

## Daily Physical Startup

```bash
uv run chess-gantry --config config.json ports
uv run chess-gantry --config config.json diagnose
uv run python scripts/check_firmware.py
uv run chess-gantry --config config.json home-gantry \
  --record data/gantry_home.json \
  --confirm-motion --confirm-clear-path
```

Test endstops without movement:

```bash
uv run chess-gantry --config config.json endstop-watch --interval 0.1
```

Expected switch names:

```text
x_min
y_max
z_max
```

## Movement And Magnet Tests

Short movement:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 5 --feed-mm-min 300 --confirm-motion
```

Magnet pulse:

```bash
uv run chess-gantry --config config.json magnet-test \
  --duration-s 1 --confirm-motion
```

Full 330 x 300 mm perimeter:

```bash
uv run chess-gantry --config config.json perimeter-demo \
  --width-mm 330 --height-mm 300 --feed-mm-min 1800 \
  --confirm-motion --confirm-clear-workspace
```

200 mm magnet circle:

```bash
uv run chess-gantry --config config.json circle-demo \
  --diameter-mm 200 --feed-mm-min 1800 --segments 72 \
  --confirm-motion --confirm-clear-workspace --confirm-magnet
```

## Plan And Execute Moves

Plan without moving hardware:

```bash
uv run chess-gantry --config config.json \
  plan examples/move_e2_e4.json --summary-json
```

Execute only after inspecting the plan and matching physical/JSON state:

```bash
uv run chess-gantry --config config.json \
  execute examples/move_e2_e4.json --confirm-motion
```

Capturing moves are rejected while physical capture slots remain disabled.

## Lichess

The default game ID is `6RkOwfp1`.

```bash
./scripts/lichess_game.sh check
./scripts/lichess_game.sh dry-run
```

For physical following, restore a standard board and then run:

```bash
./scripts/lichess_game.sh reset
./scripts/lichess_game.sh play
```

Normal moves, en passant conversion, and castling planning are supported by the
software, but physical captures require configured capture storage and promotion
requires physical piece replacement.

### Live Lichess TV Demo

The browser dashboard has a dedicated **Live Lichess TV game** panel for a
fresh public game. It is designed for a presentation where the board begins in
the standard position and every new Lichess move should reach the gantry with
minimal delay.

Physical orientation:

```text
h1 is the square closest to home on White's side.
h1 raw center: X2 Y298 Z320
a1 raw center: X2 Y298 Z40
h8 raw center: X282 Y18 Z320
a8 raw center: X282 Y18 Z40
```

Start the authenticated network UI on the gantry computer:

```bash
./scripts/run_network_ui.sh
```

Then:

1. Create a new public standard chess game on Lichess.
2. Do not make the first move yet.
3. Put every physical piece in its standard starting square.
4. Open the authenticated dashboard URL on the TV/demo control device.
5. Enter the 8-12 character Lichess game ID from the game URL.
6. Check **Board is reset to the standard starting position**.
7. Check **Paths are clear and physical motion is approved**.
8. Press **Start immediate live play**.
9. Wait for the state to show `following`.
10. Play the game on Lichess.

The web server creates a fresh isolated JSON state directory for every Start,
homes the gantry once, opens Lichess's streaming game-move API, and executes
each newly published ply through one persistent serial connection. It does not
use the older fixed polling interval, so the only normal delay is Lichess event
delivery, planning, serial transmission, and physical motion.

Start is rejected if the game already contains moves. This avoids replaying an
existing game onto a freshly reset physical board. Stop and restart with a new
empty game if needed.

State and logs are per web-server process and per Start. Restarting the web
server or pressing Start for another game creates a new standard state; no move
history from the previous TV session is reused.

The panel displays:

- current state (`starting`, `homing`, `following`, `executing`, `failed`)
- executed move count
- last stable event ID
- live execution log

Press **Stop live game** to stop the stream and attempt `M112`. Reset and re-home
the controller afterward.

> [!WARNING]
> Physical capture storage is disabled for the measured 40 mm grid. The TV
> follower stops safely with a visible error when a capture occurs. Promotion
> also stops because it requires physical piece replacement. For a guaranteed
> uninterrupted TV sequence, use a prepared non-capturing line or add and
> calibrate external capture storage before the presentation.

## State And Recovery

Runtime state is local:

| File                     | Purpose                             |
| ------------------------ | ----------------------------------- |
| `data/board_state.json`  | Last committed physical position    |
| `data/pending_move.json` | Interrupted or unconfirmed movement |
| `data/audit.jsonl`       | Append-only operation history       |

Inspect a pending transaction:

```bash
uv run chess-gantry --config config.json reconcile
```

Mark it applied only if the physical move completed exactly:

```bash
uv run chess-gantry --config config.json reconcile \
  --mark-applied --confirm-physical-state
```

Discard it only if the board still matches committed JSON state:

```bash
uv run chess-gantry --config config.json reconcile \
  --discard --confirm-physical-state
```

Emergency stop:

```bash
uv run chess-gantry --config config.json stop
```

Reset or power-cycle Marlin and home again after `M112`.

## Architecture

```text
Move JSON / Lichess / Browser UI
                |
                v
      board-state validation
                |
                v
     collision-aware planning
                |
                v
       bounded Marlin G-code
                |
                v
 serial acknowledgements -> committed JSON
                |
                +---------> recovery journal on interruption
```

## Development

```bash
uv sync
npm ci
./scripts/check.sh
npm run check
./scripts/demo_check.sh
```

The test suite covers geometry, planning, persistence, serial protocol, firmware
configuration, web authentication, dashboard task ownership, keyboard jogging,
and all measured traversal coordinates.

## Documentation

- [RUNNING.md](./RUNNING.md) — detailed commissioning and command reference
- [LICHESS_PIPELINE.md](./LICHESS_PIPELINE.md) — replay and follow workflow
- [INTEGRATION_NOTES.md](./INTEGRATION_NOTES.md) — hardware/software boundaries
- [config.example.json](./config.example.json) — complete configuration example

Built for a chessboard that does more than wait for the next move.
