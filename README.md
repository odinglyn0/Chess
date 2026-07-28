# Chess Gantry

# A Patch Project by Basil Amin, Ben Hewston, Kelvin Gao and Odin Glynn

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
- The custom firmware identifies itself as `Relay Chess Gantry` through `M115`,
  and `config.json` requires Marlin identity verification.
- The custom firmware exposes the Creality 4.2.2 controllable fan output as
  logical fan `P0` at full PWM.
- A physical test with the electromagnet directly attached caused the USB or
  controller connection to reset under load.
- After that event, `/dev/ttyUSB0` temporarily disappeared. Always run
  `diagnose` before a presentation.

The configured magnet commands are:

```gcode
M106 P0 S255
```

Both outputs are disabled with:

```gcode
M107 P0
```

If energizing the magnet resets the controller, do not repeatedly retry it.
Drive the magnet through a correctly rated MOSFET or relay module with flyback
protection and an appropriate external supply. Use the Ender output as a control
signal and share ground where required by the driver design.

## Flash The Gantry Firmware

> [!IMPORTANT]
> No new flash is required for the 330 mm inner by 270 mm outer dimensions if
> the last working Relay Chess firmware is already installed. That firmware has
> native 350 mm limits, which safely contain the smaller physical envelope.
> Host configuration now runs native `G28 X Y Z`, waits for completion, then
> applies `G92 X2 Y268 Z328` to remap the backed-off home into the measured
> coordinate system. Every generated movement remains bounded to outer
> `0..270` and inner `0..330`.

Verify the installed firmware without flashing:

```bash
uv run python scripts/check_firmware.py
```

Test homing and the host remap:

```bash
uv run python scripts/check_firmware.py \
  --home --confirm-clear-path
```

Expected final host coordinates:

```text
X:2.00 Y:268.00 Z:328.00
```

The binary below is retained only for reproducible future rebuilds. Flashing it
is optional for this dimension change.

The flashable binary is:

```text
firmware/relay-chess-v422-stm32f103ret6.bin
```

It is built specifically for:

```text
Creality motherboard: 4.2.2
MCU: STM32F103RET6, 512 KB
Stepper-driver code: C, HR4988/A4988-compatible
Marlin source: chicken, commit 8f2968f16a
PlatformIO target: STM32F103RE_creality
```

Do not flash this binary onto a GD32, STM32F103RCT6, 4.2.7, or 8-bit board.

Verify the binary before copying it:

```bash
cd firmware
sha256sum -c relay-chess-v422-stm32f103ret6.bin.sha256
cd ..
```

The corrected inner-axis-direction binary has SHA-256:

```text
d18b76a2901b299b372d9187b030fe9bd06d258be9eaf14efc8ffe914f85430b
```

Do not flash an earlier binary with a different checksum. Earlier builds either
drove the motor on the physical E connector away from its Z end switch or used
the wrong Y-motor polarity.

Rebuild it from source when needed:

```bash
./scripts/build_firmware.sh
```

### SD-Card Flash Procedure

1. Use a FAT32-formatted microSD card, preferably 8 GB or smaller.
2. Remove old `.bin` files from the card.
3. Copy `firmware/relay-chess-v422-stm32f103ret6.bin` to the card root.
4. Rename the copied file to a short unique name not previously flashed, such
   as `RCG0727.bin`.
5. Run `sync`, then verify that the on-card file is 82,192 bytes and its SHA-256
   is `d18b76a2901b299b372d9187b030fe9bd06d258be9eaf14efc8ffe914f85430b`.
   A zero-byte file will be silently ignored by the bootloader.
6. Unmount or safely eject the card before removing it. Never unplug the reader
   immediately after `cp`.
7. Switch the Ender controller off.
8. Insert the card into the Creality 4.2.2 board.
9. Keep USB disconnected during flashing.
10. Switch the controller on and wait at least 30 seconds without interruption.
11. Switch it off, remove the card, and reconnect USB.
12. The board may rename the file to `.CUR`; that indicates the bootloader
    consumed it.

After flashing, initialize the new firmware defaults once:

```bash
uv run python - << 'PY'
from chess_gantry.config import AppConfig
from chess_gantry.serial_link import MarlinSerial

config = AppConfig.load("config.json")
with MarlinSerial(config.serial) as link:
    link.send_program(("M502", "M500", "M115", "M119", "M114"))
PY
```

`M502` is important because old printer EEPROM values can override the new
80-steps/mm gantry settings.

Verify the custom firmware identity and endstop names without movement:

```bash
uv run python scripts/check_firmware.py
```

Expected endstop names are:

```text
x_min
y_max
z_max
```

After manually testing all three switches and clearing every homing path, run
the firmware homing acceptance test:

```bash
uv run python scripts/check_firmware.py \
  --home --confirm-clear-path
```

It runs `G28 X Y Z` and requires `M114` to finish at:

```text
X:2.00 Y:268.00 Z:328.00
```

The normal application invokes the same firmware sequence with:

```bash
uv run chess-gantry --config config.json home-gantry \
  --record data/gantry_home.json \
  --confirm-motion --confirm-clear-path
```

### Firmware Wiring Contract

The custom firmware maps the machine as follows:

```text
Physical X driver -> logical X -> X-stop connector -> x_min -> homes to X=0
Physical Y driver -> logical Y -> Y-stop connector -> y_max -> homes to Y=270
Physical E driver -> logical Z -> Z-stop connector -> z_max -> homes to Z=330
Physical Z driver -> unused
```

The physical E connector is deliberately controlled with G-code `Z`, not `E`.
The pin remap is in
`chicken/Marlin/src/pins/stm32f1/pins_CREALITY_V422.h`:

```cpp
#define Z_STEP_PIN PB4
#define Z_DIR_PIN  PB3
```

`INVERT_Z_DIR` is enabled because physical testing showed that the motor on the
E connector must reverse direction to approach the Z end switch. Do not change
`Z_HOME_DIR`: the switch remains the logical `Z_MAX` end at coordinate 330.

`INVERT_X_DIR` and `INVERT_Y_DIR` are both disabled. Physical testing showed
that the two outer gantry motors must use matching electrical direction so both
sides travel together. Their logical home directions remain intentionally
different: X homes to `x_min`, while Y homes to `y_max`.

BLTouch and Z-probe homing are disabled. Extruders, hotend sensing, and bed
temperature sensing are disabled. The firmware build succeeds at 81,648 bytes
flash and 6,200 bytes RAM.

### Firmware Homing Sequence

The host sends `G28 X Y Z`. Marlin performs:

1. A simultaneous X/Y quick-home approach. X and Y each stop on their own
   hardware switch, squaring the two outer gantry sides.
2. Standard Marlin backoff and slower precision bump homing for X and Y.
3. Z homing. Logical Z drives the motor physically plugged into E until the
   switch plugged into Z-stop triggers.
4. A 2 mm post-home backoff on all three axes.
5. Final switch coordinates are `X0 Y270 Z330`; after the configured 2 mm
   safety backoff, `M114` reports `X2 Y268 Z328`.

Endstop stopping occurs inside Marlin's real-time stepper/endstop code, not by
USB polling.

The firmware enables Marlin's emergency parser. If the post-flash homing test is
interrupted with `Ctrl+C`, `scripts/check_firmware.py` sends raw `M112` before
closing the serial port. Reset or power-cycle the controller after any emergency
stop.

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

## Complete Run Order

Use this section as the normal commissioning and operating checklist. Run each
stage in order. Do not skip directly to physical chess execution on a newly
flashed or mechanically changed gantry.

### 1. Run All Non-Motion Checks

These commands do not open the physical serial port:

```bash
./scripts/check.sh
npm run check
./scripts/demo_check.sh
```

Expected results include:

```text
Ran 95 tests
OK
Steering evaluation passed.
Demo readiness checks passed. No physical serial port was opened.
```

Verify the packaged firmware image when firmware files changed:

```bash
cd firmware
sha256sum -c relay-chess-v422-stm32f103ret6.bin.sha256
cd ..
```

### 2. Power And Connect

1. Clear the gantry and keep the emergency cutoff ready.
2. Switch on the Ender 24 V supply.
3. Connect USB.
4. Verify the serial device and custom firmware:

```bash
uv run chess-gantry --config config.json ports
uv run chess-gantry --config config.json diagnose
uv run python scripts/check_firmware.py
```

Do not continue unless the firmware identifies as `Relay Chess Gantry` and
Marlin reports `x_min`, `y_max`, and `z_max`.

### 3. Test Every Endstop Without Motion

```bash
uv run chess-gantry --config config.json endstop-watch --interval 0.1
```

Press and release each switch by hand. Confirm all six transitions:

```text
HIT x_min
RELEASED x_min
HIT y_max
RELEASED y_max
HIT z_max
RELEASED z_max
```

Stop with `Ctrl+C`.

### 4. Test Firmware Homing

Remove all pieces and obstructions from every path. Run:

```bash
uv run python scripts/check_firmware.py \
  --home --confirm-clear-path
```

Expected final position after Marlin's 2 mm safety backoff:

```text
X:2.00 Y:268.00 Z:328.00
```

The physical motor plugged into E is logical Z in this firmware. If any axis
moves away from its switch, use the physical cutoff immediately.

For normal daily startup, use the application homing command instead:

```bash
uv run chess-gantry --config config.json home-gantry \
  --record data/gantry_home.json \
  --confirm-motion --confirm-clear-path
```

This runs the same Marlin `G28 X Y Z` and records `M119`/`M114` results.

### 5. Test Movement Without The Magnet

Print the G-code first:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 5 --feed-mm-min 300
```

Then run the short physical test:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 5 --feed-mm-min 300 --confirm-motion
```

After direction, scale, and return position are correct:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 20 --feed-mm-min 1200 --confirm-motion
```

### 6. Test The Electromagnet Without Movement

Print the pulse:

```bash
uv run chess-gantry --config config.json magnet-test --duration-s 1
```

Run one physical pulse:

```bash
uv run chess-gantry --config config.json magnet-test \
  --duration-s 1 --confirm-motion
```

The firmware uses `M106 P0 S255` for on and `M107 P0` for off.

### 7. Move One Piece

Generate and inspect the exact sequence:

```bash
uv run chess-gantry --config config.json piece-demo \
  --distance-mm 20 --feed-mm-min 1200 \
  --output data/piece-demo.gcode
```

The guarded physical `piece-demo` requires all three switches to be held at the
reference at command start. Place the gantry on `x_min`, `y_max`, and `z_max`,
put one piece under the magnet, clear the 20 mm path, then run:

```bash
uv run chess-gantry --config config.json piece-demo \
  --distance-mm 20 --feed-mm-min 1200 \
  --confirm-motion \
  --confirm-at-switches \
  --confirm-piece \
  --confirm-magnet
```

For a continuous presentation loop after the short piece test succeeds:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 20 --feed-mm-min 1200 \
  --magnet-on --presentation-loops 3 \
  --confirm-motion --confirm-magnet
```

### 8. Test The Full Workspace

Run this with an empty gantry workspace and the magnet off. Generate the path:

```bash
uv run chess-gantry --config config.json workspace-test \
  --feed-mm-min 1200 --margin-mm 20 \
  --columns 8 --rows 8 --dwell-ms 100 \
  --output data/workspace-test.gcode
```

Place all three axes against their switches, verify them with `endstop-watch`,
then execute:

```bash
uv run chess-gantry --config config.json workspace-test \
  --feed-mm-min 1200 --margin-mm 20 \
  --columns 8 --rows 8 --dwell-ms 100 \
  --confirm-motion \
  --confirm-empty-workspace \
  --confirm-at-switches
```

### 8a. Run The 20 cm Magnet Circle

`circle-demo` interprets 20 cm as a 200 mm diameter. It homes with Marlin,
energizes fan `P0`, approaches a circle centered at logical `(250, 250)`, traces
72 linear segments, switches the magnet off, returns to `X0 Y270 Z330`, and
disables the motors.

Generate and inspect the G-code without connecting:

```bash
uv run chess-gantry --config config.json circle-demo \
  --diameter-mm 200 \
  --feed-mm-min 1800 \
  --segments 72 \
  --output data/circle-demo.gcode
```

Simulate the complete stream:

```bash
uv run chess-gantry --config config.demo.json circle-demo \
  --diameter-mm 200 \
  --feed-mm-min 1800 \
  --segments 72 \
  --confirm-motion \
  --demo
```

For physical execution, remove every piece and obstruction from the complete
200 mm circle and its approach path. Keep the emergency cutoff ready. The
magnet remains energized for approximately 22 seconds at 1,800 mm/min.

```bash
uv run chess-gantry --config config.json circle-demo \
  --diameter-mm 200 \
  --feed-mm-min 1800 \
  --segments 72 \
  --confirm-motion \
  --confirm-clear-workspace \
  --confirm-magnet
```

The command refuses circles outside the configured workspace, fewer than 12 or
more than 360 segments, feed rates above the configured travel feed, or magnet
energization estimates above 30 seconds. On serial failure it attempts to turn
the magnet off and disable the motors.

### 8b. Trace The Board Perimeter

`perimeter-demo` homes first and treats the home point as the first corner. It
traces the complete 330 mm inner by 270 mm outer machine envelope, closes the
rectangle at `X0 Y270 Z330`, and disables the motors. The physical sequence is:

```text
X0 Y270 Z330 -> X0 Y270 Z0 -> X270 Y0 Z0
              -> X270 Y0 Z330 -> X0 Y270 Z330
```

Generate and inspect it without connecting:

```bash
uv run chess-gantry --config config.json perimeter-demo \
  --width-mm 330 \
  --height-mm 270 \
  --feed-mm-min 1800 \
  --output data/perimeter-demo.gcode
```

Simulate it:

```bash
uv run chess-gantry --config config.demo.json perimeter-demo \
  --width-mm 330 \
  --height-mm 270 \
  --feed-mm-min 1800 \
  --confirm-motion \
  --demo
```

Clear the complete 330 x 270 mm rectangle and keep the emergency cutoff ready,
then run it physically with the magnet off:

```bash
uv run chess-gantry --config config.json perimeter-demo \
  --width-mm 330 \
  --height-mm 270 \
  --feed-mm-min 1800 \
  --confirm-motion \
  --confirm-clear-workspace
```

The magnet is off by default. A magnet-on perimeter is allowed only when the
estimated hold is at most 30 seconds, so this 330 x 270 mm perimeter requires
at least 2,000 mm/min. The documented magnet variant uses 3,000 mm/min:

```bash
uv run chess-gantry --config config.json perimeter-demo \
  --width-mm 330 \
  --height-mm 270 \
  --feed-mm-min 3000 \
  --magnet-on \
  --confirm-motion \
  --confirm-clear-workspace \
  --confirm-magnet
```

### 9. Run The Browser Software

Simulated UI:

```bash
./scripts/live_demo.sh
```

Physical UI:

```bash
uv run chess-gantry --config config.json web
```

Open <http://127.0.0.1:8000>. Home before executing physical moves.

The browser now includes an **Operations dashboard** with live task output and
one-click allowlisted workflows for:

- all tests, formatting checks, and complete demo readiness
- simulated circle and perimeter demos
- installed-firmware and endstop checks
- physical homing and short movement tests
- magnet pulse, circle, perimeter, workspace-grid, and piece demos
- board JSON inspection, reset, and pending-move reconciliation
- Lichess check, dry-run follower, and physical play

Physical task cards display required confirmation checkboxes and a second
browser confirmation. Only one dashboard task can run at a time. Serial tasks
disconnect the browser's persistent serial connection before starting so two
processes cannot own `/dev/ttyUSB0` simultaneously.

The **Stop task** button terminates the complete subprocess tree. For a physical
task it also attempts `M112`; reset or power-cycle and re-home afterward.

For a UI that cannot run real hardware, launch:

```bash
uv run chess-gantry --config config.demo.json web --demo
```

Physical operation cards are disabled at the server layer in `--demo` mode,
not just hidden in the browser.

The server binds only to `127.0.0.1` by default. Network mode requires both
`--allow-network` and a strong access token.

### Authenticated Network UI

To let other devices on the same trusted LAN use the UI while commands and
serial access remain on this computer, run:

```bash
./scripts/run_network_ui.sh
```

The launcher:

- generates a new random 256-bit access token for each start
- binds the server to `0.0.0.0:8000`
- prints a complete authenticated URL using this computer's LAN address
- keeps all shell commands and `/dev/ttyUSB0` access on this computer

Open the complete printed URL on another device. It looks like:

```text
http://192.168.1.50:8000/?token=LONG_RANDOM_TOKEN
```

The first request stores the token in an `HttpOnly; SameSite=Strict` cookie and
redirects to `/`, removing the token from the address bar. Every page and API
request requires the token. Bad or missing tokens receive HTTP 401. Tokens are
redacted from server request logs.

To use a fixed token and another port:

```bash
CHESS_GANTRY_WEB_TOKEN="$(uv run python -c 'import secrets; print(secrets.token_urlsafe(32))')" \
CHESS_GANTRY_WEB_PORT=8080 \
  ./scripts/run_network_ui.sh
```

On Fedora, if another device cannot connect, open the selected TCP port for the
current firewalld zone:

```bash
sudo firewall-cmd --add-port=8000/tcp
```

Remove the temporary firewall rule after the session:

```bash
sudo firewall-cmd --remove-port=8000/tcp
```

Do not add `--permanent` unless this service should remain exposed after
reboot. Do not port-forward this service through the router or expose it to the
internet. Token authentication protects commands but plain HTTP does not encrypt
the token or traffic; use only a trusted private LAN or place the service behind
a TLS VPN/reverse proxy.

Stop the server with `Ctrl+C`. Long-running dashboard tasks are terminated on
server shutdown. Cancelled physical tasks also attempt `M112`, after which the
controller must be reset and re-homed.

### 10. Run A Planned Chess Move

The checked-in physical chess-square geometry must be measured before this
stage. Dry-run the included move:

```bash
uv run chess-gantry --config config.json \
  plan examples/move_e2_e4.json --summary-json
```

After calibration, reset the physical and JSON boards to the standard position,
home, then execute:

```bash
uv run chess-gantry --config config.json reset-state \
  --confirm-standard-position

uv run chess-gantry --config config.json home-gantry \
  --record data/gantry_home.json \
  --confirm-motion --confirm-clear-path

uv run chess-gantry --config config.json execute \
  examples/move_e2_e4.json --confirm-motion
```

### 11. Run Lichess Game `6RkOwfp1`

Dry-run first:

```bash
./scripts/lichess_game.sh check
./scripts/lichess_game.sh dry-run
```

Stop the follower with `Ctrl+C`, physically restore the standard board, then:

```bash
./scripts/lichess_game.sh reset
./scripts/lichess_game.sh play
```

`play` homes the gantry before starting the physical follower.

### 12. Stop Or Recover

Emergency stop:

```bash
uv run chess-gantry --config config.json stop
```

Reset or power-cycle Marlin after `M112`.

Inspect an interrupted move:

```bash
uv run chess-gantry --config config.json reconcile
```

Only after physically checking the board, mark it applied or discard it using
the recovery commands later in this README.

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

The presentation mode repeats a fixed four-leg path while keeping fan `P0` at
full power. It refreshes `M106 P0 S255` before every movement leg and sends no
`M107 P0` until the final return.

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
- refreshes `P0` at `S255` before each leg
- turns the output off after the final movement
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

### Watch Endstop Switches

Keep the motors stationary and run:

```bash
uv run chess-gantry --config config.json endstop-watch
```

The command polls Marlin `M119` every 200 ms and prints the initial state plus
every transition immediately. Press and release each switch by hand. Example:

```text
Watching endstops on /dev/ttyUSB0 at 115200 baud; press Ctrl+C to stop.
INITIAL x_min OPEN
INITIAL y_max OPEN
INITIAL z_max OPEN
HIT x_min
RELEASED x_min
HIT y_max
RELEASED y_max
HIT z_max
RELEASED z_max
```

Stop with `Ctrl+C`. To poll more slowly:

```bash
uv run chess-gantry --config config.json endstop-watch --interval 0.5
```

To take exactly ten samples and exit:

```bash
uv run chess-gantry --config config.json endstop-watch --samples 10
```

Run a serial-free parser check with simulated open switches:

```bash
uv run chess-gantry --config config.demo.json endstop-watch \
  --demo --samples 3 --interval 0.05
```

For independent X/Y gantry alignment, one switch must report for each motor
side. Both expected switches should be `TRIGGERED` when the mechanism is
physically square at the homing end. A single switch total cannot prove that
two independently driven sides are aligned.

On this machine the inner gantry motor is physically connected to the E driver,
but the custom firmware exposes it as logical Z. The complete reference is:

```text
x_min TRIGGERED -> first outer gantry motor at its end
y_max TRIGGERED -> second outer gantry motor at its end
z_max TRIGGERED -> inner carriage on the physical E driver
```

Manually hold all three carriages against their switches, verify all three with
`endstop-watch`, then assign the mirrored software reference without moving:

```bash
uv run chess-gantry --config config.json reference-gantry \
  --confirm-at-switches
```

The command refuses unless Marlin reports `x_min`, `y_max`, and `z_max` as
`TRIGGERED`. The switch reference is `X=0`, `Y=workspace max`, and
`Z=workspace max`. It does not drive toward the switches.

### Automatic Gantry Homing

The Ender firmware contains the complete homing sequence. `home-gantry` does
not choose directions, speeds, distances, backoff, or coordinates. It switches
the magnet output off and sends the commands listed in
`safety.home_commands`. The checked-in physical configuration uses `G28 X Y Z`
followed by `M400`.

Before running:

- clear all three paths to the switches
- keep the emergency power cutoff ready
- verify pressing each switch produces the expected `HIT` in `endstop-watch`
- make sure no belt, carriage, cable, or piece can snag during homing

Then run:

```bash
uv run chess-gantry --config config.json home-gantry \
  --record data/gantry_home.json \
  --confirm-motion \
  --confirm-clear-path
```

The host sends exactly:

```gcode
M107 P0
G21
G28 X Y Z
M400
M119
M114
```

Marlin performs all real-time endstop handling. After `G28` completes, the host
records the raw `M119` endstop report and `M114` coordinates in
`data/gantry_home.json`. No host-generated `G1` or `G92` command is part of this
homing path.

If `G28` or either verification command fails, no homing record is written and
the host attempts to switch the magnet output off and disable motors.

The previous stock firmware entered a BLTouch routine and failed. The custom
firmware in `chicken` disables BLTouch, remaps the physical E driver to logical
Z, and uses the mechanical Z-stop switch directly.

The record is evidence of the last successful homing operation; it cannot prove
that the gantry has not been manually moved or lost steps afterward. Home again
after power loss, motor disable, collision, manual movement, or controller
reset.

This watcher is a stationary wiring and switch test. Do not use host-side
`M119` polling to stop moving motors: USB latency is not deterministic. Real
homing and endstop stopping must be configured and executed inside Marlin
firmware, followed by host-side verification with `M119` and `M114`.

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

The command sends fan `P0` off before the pulse, drives it at full PWM, and
sends it off afterward. Magnet-only pulses are limited to five
seconds.

### Pickup, Move, Release, Return

The dedicated `piece-demo` combines all three endstops, gantry movement, and
the electromagnet in one guarded test. It requires `x_min`, `y_max`, and
`z_max` to be triggered immediately before movement.

Print the exact test without connecting:

```bash
uv run chess-gantry --config config.json piece-demo \
  --distance-mm 20 --feed-mm-min 1200 \
  --output data/piece-demo.gcode
```

Simulate the complete command stream:

```bash
uv run chess-gantry --config config.demo.json piece-demo \
  --distance-mm 20 --feed-mm-min 1200 \
  --confirm-motion --demo
```

For the physical test:

1. Correct the electromagnet driver if direct coil load still resets the Ender
   controller.
2. Clear a 20 mm by 20 mm path away from the switches.
3. Manually place both outer sides and the inner Z carriage on their
   X/Y/Z switches.
4. Put one piece directly beneath the magnet at that reference position.
5. Verify all three switches are `TRIGGERED` with `endstop-watch`.
6. Keep an independent emergency cutoff ready.
7. Run:

```bash
uv run chess-gantry --config config.json piece-demo \
  --distance-mm 20 --feed-mm-min 1200 \
  --confirm-motion \
  --confirm-at-switches \
  --confirm-piece \
  --confirm-magnet
```

The command queries `M119` again and refuses to move unless all three switches
remain triggered. It then assigns `X0 Y270 Z330`, energizes fan `P0` at full
PWM, moves inner `Z` to 310 mm, moves the aligned outer pair to `X20 Y250`,
releases the piece, and returns to `X0 Y270 Z330` with the magnet off.
It finishes by disabling the motors and does not modify chess-state JSON.

The test is deliberately limited to a short transfer. Do not increase distance
or duration until the 20 mm test works without controller resets, missed steps,
or loss of magnet holding force.

### Generic Motor Test

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

### Full Workspace Movement Test

Use this test before relying on the chess-square geometry. It traverses an 8 x
8 serpentine grid over the configured 330 x 270 mm usable workspace with a 20
mm edge margin, pauses at every point, and returns to the three-switch
reference. The electromagnet remains off.

Generate and inspect the G-code without connecting:

```bash
uv run chess-gantry --config config.json workspace-test \
  --feed-mm-min 1200 \
  --margin-mm 20 \
  --columns 8 \
  --rows 8 \
  --dwell-ms 100 \
  --output data/workspace-test.gcode
```

Simulate it:

```bash
uv run chess-gantry --config config.demo.json workspace-test \
  --feed-mm-min 1200 \
  --margin-mm 20 \
  --columns 8 \
  --rows 8 \
  --dwell-ms 100 \
  --confirm-motion --demo
```

For physical execution:

1. Remove every piece and obstruction from the complete configured workspace.
2. Manually place both outer sides and the inner carriage against their X, Y,
   and Z switches.
3. Verify all three show `TRIGGERED` with `endstop-watch`.
4. Keep the emergency power cutoff ready.
5. Run:

```bash
uv run chess-gantry --config config.json workspace-test \
  --feed-mm-min 1200 \
  --margin-mm 20 \
  --columns 8 \
  --rows 8 \
  --dwell-ms 100 \
  --confirm-motion \
  --confirm-empty-workspace \
  --confirm-at-switches
```

Immediately before movement, the command queries `M119` and refuses to continue
unless `x_min`, `y_max`, and `z_max` are all triggered. This command uses a
manual switch reference and is separate from automatic firmware homing, whose
configured 2 mm backoff leaves the switches open.

### Chess-Square Sweep

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

The calibrated machine envelope is:

```text
Inner gantry / logical Z width: 330 mm
Outer paired X/Y gantry height: 270 mm
```

Chess squares must remain square, so the 8 x 8 playing grid is 270 x 270 mm,
using 33.75 mm squares. It is centered across the 330 mm width with 30 mm side
margins. The `a1` square center is at logical `(46.875, 16.875)`.

If the mechanics change, remeasure and update:

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

`config.demo.json` uses the same 330 x 270 mm envelope and centered chess-grid
geometry as the physical configuration.

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

`play` runs `home-gantry` first and saves a game-specific record at
`data/lichess/6RkOwfp1/gantry_home.json`. The Lichess follower starts only if all
three switches trigger and homing completes successfully.

Home separately before the game with:

```bash
./scripts/lichess_game.sh home
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

Treat this as an electrical load or interference problem. Switch fan `P0`
off, power-cycle the controller, and correct the magnet driver circuit. Do not
solve a controller reset by increasing pulse duration or repeatedly retrying
full power.

### LCD Still Shows Fan 0

Connector labels and Marlin logical indices differ across Ender boards and
firmware. The custom firmware exposes the controllable output as `P0`, so Fan 0
on the LCD is expected. Verify the electrical output with a meter and the board
schematic rather than relying only on the connector label.

### Pending Transaction Error

Run `reconcile`, inspect the stored transaction, physically inspect the board,
and then explicitly mark it applied or discard it.

## Current Verification

The latest completed verification included:

- 95 automated tests passing
- Python compilation passing
- Black and Prettier checks passing
- repository policy checks passing
- exact presentation G-code ordering tests passing
- simulated continuous-power presentation streaming passing
- single `P0` magnet command tests passing
- custom Marlin 4.2.2 firmware build passing
- emergency parser and corrected logical-Z direction assertions passing
- packaged firmware SHA-256 verification passing
- JSON restart persistence passing
- public Lichess polling and PGN planning passing
- browser demo API startup passing

The custom firmware, homing sequence, and bootloader-compatible SD-card process
have been physically validated. Electromagnet power reliability still depends
on the external driver, flyback protection, and supply wiring.

Additional direct-command details are available in [RUNNING.md](RUNNING.md).
