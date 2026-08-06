# Running Chess Gantry

Run all commands from the repository root. State is stored only in local JSON
and JSONL files.

## Raspberry Pi Docker Deployment

Raspberry Pi OS Lite does not need host `uv` or Node.js. Install Docker and
build/start the container with:

```bash
sudo apt update
sudo apt install -y git curl
git clone --recurse-submodules https://github.com/odinglyn0/Chess.git
cd Chess
./scripts/install_pi.sh
```

The service exposes the authenticated dashboard on port 8000, passes the host
`/dev/ttyUSB0` into the container, mounts `config.json` read-only, and persists
JSON state under host `data/`.

Ubuntu 24.04 is used only as the build stage. The production image is based on
`gcr.io/distroless/cc-debian12`, with a uv-managed CPython 3.11 environment
and the `uv` binary copied into runtime. There is no runtime shell or package
manager.

```bash
./scripts/pi_docker.sh status
./scripts/pi_docker.sh logs
./scripts/pi_docker.sh firmware-check
./scripts/pi_docker.sh test
./scripts/pi_docker.sh check
./scripts/pi_docker.sh restart
./scripts/pi_docker.sh update
./scripts/pi_docker.sh down
```

If the serial device uses another path, set `CHESS_GANTRY_SERIAL_DEVICE` before
running `install_pi.sh`, or update `.env.docker` and recreate the service.

The serial device must exist when Compose starts the container. After changing
the USB path, recreate with `./scripts/pi_docker.sh down` followed by
`./scripts/pi_docker.sh up`.

For future deployments after pushing changes:

```bash
cd ~/Chess
./scripts/pi_docker.sh update
```

This performs a fast-forward-only pull, updates submodules, rebuilds using the
Ubuntu stage, and recreates the distroless runtime while preserving `data/` and
`.env.docker`.

## Current Dimensions Without Reflashing

The installed working firmware may retain native 350 mm axis limits. No reflash
is required for the measured smaller machine envelope:

```text
Inner gantry / logical Z width: 330 mm
Outer paired X/Y gantry height: 300 mm
```

Every configured home runs:

```gcode
G28 X Y Z
M400
G92 X2 Y298 Z328
M400
```

The `G92` remap converts the installed firmware's backed-off home into the new
physical coordinates. Host-generated movement is restricted to X/Y `0..300`
and Z `0..330`.

The measured square centers use exact 40 mm spacing. Logical centers span inner
40..320 mm and outer 18..298 mm. The four raw Marlin corner centers are
`X2 Y298 Z320`, `X282 Y18 Z320`, `X282 Y18 Z40`, and `X2 Y298 Z40`.

## Install And Verify

```bash
uv sync
npm ci
./scripts/demo_check.sh
```

`demo_check.sh` runs the complete test and policy suites, plans `e2e4`, tests
the electromagnet output against simulated Marlin, and streams a simulated
64-square sweep.

## Container On A Raspberry Pi 3B+

The image is built by a Fedora builder that resolves dependencies with `uv` from
`uv.lock`, then hands a complete root filesystem to a `scratch` runner. The
runner carries Python, curl, the CA trust store, tzdata and the application. It
has no shell and no package manager.

Only `linux/arm64` is produced, so the Pi must run a 64-bit OS. Fedora has
published no 32-bit arm tree since Fedora 37, so there is no armv7 builder.

Enable the buses the container expects, then reboot:

```text
/boot/firmware/config.txt
dtparam=i2c_arm=on
dtparam=spi=on
```

Prepare the host and build:

```bash
./scripts/docker_host_setup.sh
docker compose build
docker compose up -d gantry
```

`docker_host_setup.sh` writes the real `dialout`, `gpio`, `i2c` and `spi` group
IDs into `.env`, confirms every passed-through device node exists, creates
`config.json` and `data/`, and refuses to pass a host that is not ready.

### What Is Passed Through

| Path                               | Purpose                                |
| ---------------------------------- | -------------------------------------- |
| `/dev/ttyUSB0`                     | Marlin serial link                     |
| `/dev/bus/usb`                     | USB re-enumeration after a magnet drop |
| `/dev/gpiomem`, `/dev/gpiochip0`   | GPIO, memory-mapped and character      |
| `/dev/i2c-1`                       | I2C bus 1                              |
| `/dev/spidev0.0`, `/dev/spidev0.1` | SPI chip selects 0 and 1               |

Character-major cgroup rules accompany the device list, so a controller that
re-enumerates as a different node stays reachable without recreating the
container. The container runs as UID 65532 with a read-only root filesystem, all
capabilities dropped, and `no-new-privileges`. It reaches the devices through the
supplementary groups in `.env`, not through `--privileged`.

`RPi.GPIO`, `gpiozero`, `smbus2` and `spidev` are installed for GPIO, I2C and
SPI work. Build with `INCLUDE_GPIO=0` to leave them out.

### Reaching The Dashboard

`docker compose up -d gantry` publishes port 8000 on every host interface, so the
dashboard answers on loopback and across the LAN. The application refuses a
non-loopback bind without a token; set `CHESS_GANTRY_WEB_TOKEN` in `.env` or read
the token the entrypoint generates:

```bash
docker compose logs gantry | grep 'access token'
```

For a first-class intranet address instead of a published host port, fill in
`LAN_PARENT`, `LAN_SUBNET`, `LAN_GATEWAY` and `LAN_IP`, then start the macvlan
service:

```bash
docker compose --profile lan up -d gantry-lan
```

This is plain HTTP. Keep it off the public internet.

### Debug Console

The console owns the same serial port, so run it instead of `gantry`, never
alongside it:

```bash
docker compose stop gantry
docker compose --profile console up -d console
docker compose logs console | grep 'access token'
```

### Other Commands

Any CLI subcommand runs in the container with the correct state paths already
applied:

```bash
docker compose run --rm gantry ports
docker compose run --rm gantry diagnose
docker compose run --rm gantry show-state
docker compose run --rm gantry plan examples/move_e2_e4.json --summary-json
docker compose run --rm gantry stop
```

### Dashboard Buttons That Need A Shell

**Run all tests**, **Formatting and policy** and **Complete demo readiness**
shell out to `scripts/*.sh` and `npm`, which the distroless runner does not
carry. Build with `INCLUDE_DEV_TOOLS=1` to add bash, Node and npm for those
buttons. That image is no longer distroless, so keep the default of `0` for
deployment and run those checks on a development machine with `uv` and `npm`.

Everything else that shells out works, because `uv` resolves to a shim that
drops `uv run` and execs the real target: `uv sync` is a no-op, and
`uv run chess-gantry ...` and `uv run python scripts/check_firmware.py` behave as
they do outside the container.

## Local Files

Global defaults:

```text
--state data/board_state.json
--journal data/pending_move.json
--audit data/audit.jsonl
```

Override these before the command when isolating a game:

```bash
uv run chess-gantry \
  --config config.json \
  --state data/games/example/board_state.json \
  --journal data/games/example/pending_move.json \
  --audit data/games/example/audit.jsonl \
  show-state
```

## Lichess Game 6RkOwfp1

The helper uses `6RkOwfp1` by default and stores everything under
`data/lichess/6RkOwfp1/`.

```bash
./scripts/lichess_game.sh check
./scripts/lichess_game.sh dry-run
./scripts/lichess_game.sh status
./scripts/lichess_game.sh reset
./scripts/lichess_game.sh play
./scripts/lichess_game.sh reconcile
```

`check` runs software readiness and replays the current public PGN without
hardware. `dry-run` continuously polls and writes plans. `play` continuously
polls and executes new moves over serial. `reset` requires the physical pieces
to be in the standard position and clears follow sessions.

The equivalent physical play command is:

```bash
uv run chess-gantry \
  --config config.json \
  --state data/lichess/6RkOwfp1/board_state.json \
  --journal data/lichess/6RkOwfp1/pending_move.json \
  --audit data/lichess/6RkOwfp1/audit.jsonl \
  lichess-follow 6RkOwfp1 \
  --output-dir data/lichess/6RkOwfp1/physical \
  --session data/lichess/6RkOwfp1/physical.session.json \
  --interval 2 --execute --confirm-motion
```

Start with a standard physical board and a reset JSON state. Keep the command
running. Successfully executed event IDs in `board_state.json` prevent replay
after restart.

## Web TV Live Game

Use the web dashboard for the lowest-latency presentation workflow:

```bash
./scripts/run_network_ui.sh
```

Create a new public Lichess game with zero moves, reset the physical board, and
enter the game ID in **Live Lichess TV game**. Confirm the board and motion,
then press **Start immediate live play** before White's first move.

The nearest-home square is h1 at raw `X2 Y298 Z320`. The server creates fresh
standard JSON state for each Start, homes once, and uses Lichess's streaming API
to trigger immediate PGN processing and physical execution. A game that already
contains moves is rejected rather than replayed.

Captures currently stop the follower because physical capture slots are
disabled. Promotion also requires manual piece replacement and is rejected.

## Reset

Arrange the physical board in its standard starting position, then run:

```bash
uv run chess-gantry --config config.json \
  reset-state --confirm-standard-position
```

For game `6RkOwfp1`:

```bash
./scripts/lichess_game.sh reset
```

Never reset while a movement or follower process is running.

## Recover A Pending Move

Inspect the journal:

```bash
uv run chess-gantry --config config.json reconcile
```

If the physical move completed exactly as shown:

```bash
uv run chess-gantry --config config.json reconcile \
  --mark-applied --confirm-physical-state
```

If it did not complete and the physical board still matches `board_state.json`:

```bash
uv run chess-gantry --config config.json reconcile \
  --discard --confirm-physical-state
```

For `6RkOwfp1`, add its state paths as shown in the physical play command.

## Plan And Execute One Move

Plan without serial or state mutation:

```bash
uv run chess-gantry --config config.json \
  plan examples/move_e2_e4.json --summary-json
```

Execute and commit JSON state only after all Marlin acknowledgements:

```bash
uv run chess-gantry --config config.json \
  execute examples/move_e2_e4.json --confirm-motion
```

## Browser Controller

Simulated:

```bash
./scripts/live_demo.sh
```

Physical:

```bash
uv run chess-gantry --config config.json web
```

Open <http://127.0.0.1:8000>. Add `--no-browser` for headless startup.

### Keyboard Jog And Live Position

After connecting and homing, the browser can jog the gantry with:

```text
Arrow Left / Right -> inner gantry width
Arrow Up / Down    -> paired outer gantry height
Escape             -> disarm keyboard movement
```

Check **Enable arrow-key motion** before using the keyboard. Select a 0.5, 1,
5, or 10 mm step and a bounded feed rate. Arrow-key events are ignored while a
form input has focus, while a key is held down, while disconnected/unhomed, or
while another dashboard task owns the serial port. A single jog is limited to
20 mm, one logical axis, and the configured 330 x 300 mm workspace.

The **Live Marlin position** box polls `M114` about every 750 ms when connected
and idle. It displays raw machine coordinates for outer X, outer Y, and inner
Z. Use **Read M114 now** for an immediate refresh.

### Authenticated LAN Access

```bash
./scripts/run_network_ui.sh
```

Open the complete token URL printed by the launcher from another device on the
same trusted LAN. The first request stores the token in an HttpOnly strict
cookie. Missing or incorrect tokens receive HTTP 401. All commands and
`/dev/ttyUSB0` access remain on the gantry computer.

If Fedora blocks port 8000 temporarily allow it with:

```bash
sudo firewall-cmd --add-port=8000/tcp
```

Remove the rule after the session:

```bash
sudo firewall-cmd --remove-port=8000/tcp
```

Do not expose the plain-HTTP dashboard to the internet.

## Shared Raw G-code Debug Console

A Django console for the machine that physically owns the serial link. It shares
one Marlin connection, streams raw G-code, and broadcasts every command and
response to all connected clients.

```bash
uv sync --extra debug-console
```

Simulated:

```bash
uv run chess-gantry --config config.demo.json debug-console --demo
```

Physical, local only:

```bash
uv run chess-gantry --config config.json debug-console
```

Physical, reachable by other machines on the network:

```bash
uv run chess-gantry --config config.json debug-console \
  --host 0.0.0.0 --allow-network --no-browser
```

Open <http://127.0.0.1:8300>. The console refuses a non-loopback bind without
`--allow-network`, and every request needs a shared access token. The token
comes from `--token`, then `$CHESS_GANTRY_DEBUG_TOKEN`, otherwise a fresh one is
generated and printed at startup. Browsers paste it into the session panel;
scripts send it as a header:

```bash
curl -X POST http://192.168.0.10:8300/api/gcode \
  -H "X-Gantry-Token: $CHESS_GANTRY_DEBUG_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"commands": ["M114", "M119"], "client": "bench-laptop"}'
```

Anyone holding the token can move the gantry, so the token is the only thing
standing between the network and the hardware. Raw commands bypass workspace,
magnet, and board-state checks. The configured emergency stop command is
rejected on the raw path; use the dedicated stop control, which closes the link
and records the reset requirement. Every command, response, and client is
appended to the audit log.

## Movement And Magnet Tests

Print only:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 5 --feed-mm-min 300
uv run chess-gantry --config config.json magnet-test --duration-s 1
uv run chess-gantry --config config.json board-sweep \
  --feed-mm-min 1800 --magnet-on
```

Measured square-center traversal:

```bash
uv run chess-gantry --config config.json square-center-demo \
  --feed-mm-min 1800 --dwell-ms 150
```

Physical traversal with the magnet continuously on:

```bash
uv run chess-gantry --config config.json square-center-demo \
  --feed-mm-min 1800 --dwell-ms 150 --magnet-on \
  --confirm-motion --confirm-clear-workspace --confirm-magnet
```

Simulated Marlin:

```bash
uv run chess-gantry --config config.demo.json motor-test \
  --distance-mm 20 --feed-mm-min 600 --confirm-motion --demo
uv run chess-gantry --config config.demo.json magnet-test \
  --duration-s 1 --confirm-motion --demo
uv run chess-gantry --config config.demo.json board-sweep \
  --feed-mm-min 1800 --magnet-on --confirm-motion --demo
```

Physical full-board sweep after calibration, clearing the board, and placing
the gantry at the configured origin:

```bash
uv run chess-gantry --config config.json board-sweep \
  --feed-mm-min 1800 --magnet-on \
  --confirm-motion --confirm-empty-board \
  --confirm-origin --confirm-magnet
```

## Emergency Stop

```bash
uv run chess-gantry --config config.json stop
```

Marlin normally requires a reset afterward.
