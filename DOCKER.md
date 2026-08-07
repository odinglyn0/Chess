# Docker

Build and run the `chess:latest` image on a Raspberry Pi, with GPIO and the Marlin serial link passed through and the web dashboard published on the LAN.

The runtime stage is built `FROM scratch`, so the image has no shell. Everything below uses `docker logs`, `docker inspect` and rebuilds instead of `docker exec ... bash`.

## Requirements

- 64-bit Raspberry Pi OS. The image is Fedora-based and Fedora publishes no 32-bit armhf builds, so a 32-bit Pi OS install cannot run it.
- Docker Engine with the Compose plugin: `./scripts/install_pi.sh` installs both.
- I2C and SPI enabled in `/boot/firmware/config.txt` (`dtparam=i2c_arm=on`, `dtparam=spi=on`) followed by a reboot, but only if the build uses those buses. Without it the `/dev/i2c-*` and `/dev/spidev*` nodes do not exist.

Build on the Pi itself. Cross-building from an x86_64 host produces an amd64 image that will not start on ARM.

## Build

```bash
docker build \
  --tag chess:latest \
  --build-arg FEDORA_VERSION=42 \
  --build-arg INCLUDE_GPIO=1 \
  --build-arg INCLUDE_DEV_TOOLS=0 \
  .
```

Expect 15 minutes or more on a Pi 3B+, most of it spent compiling wheels.

Build arguments worth changing:

| Argument             | Default | Effect                                                                                                                   |
| -------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------ |
| `INCLUDE_GPIO`       | `1`     | Installs `RPi.GPIO`, `gpiozero`, `smbus2` and `spidev`. Set to `0` for a dashboard-only image on non-Pi hardware.        |
| `INCLUDE_DEV_TOOLS`  | `0`     | Adds bash, coreutils, node and npm so the dashboard's test and formatting buttons work. Leaves the image non-distroless. |
| `FEDORA_VERSION`     | `42`    | Base image tag for both stages.                                                                                          |
| `APP_UID`, `APP_GID` | `65532` | Identity the container runs as. Anything mounted read-write must be owned by this UID.                                   |

The build fails fast rather than shipping something broken: it verifies the builder and runtime Python minor versions match, imports every runtime module inside the new rootfs, checks the CA bundle loads, and parses `config.example.json`.

## One-time host setup

The container runs as UID and GID 65532 and cannot write a root-owned directory, so `data/` has to be handed over explicitly.

```bash
cp -n config.example.json config.json
mkdir -p data
cp -n examples/board_state.standard.json data/board_state.json
sudo chown -R 65532:65532 data
```

Calibrate `config.json` for the physical gantry before driving hardware. The entrypoint warns in the log when it is missing but still starts.

## Run

```bash
docker run -d --name chess-gantry --restart unless-stopped \
  --device /dev/ttyUSB0 \
  --device /dev/gpiomem \
  --device /dev/gpiochip0 \
  --group-add "$(stat -c '%g' /dev/ttyUSB0)" \
  --group-add "$(stat -c '%g' /dev/gpiomem)" \
  --group-add "$(stat -c '%g' /dev/gpiochip0)" \
  --publish 8000:8000 \
  --volume "$PWD/config.json:/app/config.json:ro" \
  --volume "$PWD/data:/app/data" \
  chess:latest web
```

`--device` makes a node visible; `--group-add` is what makes it usable. The nodes are owned by `dialout` (serial) and `gpio` (GPIO), and UID 65532 belongs to neither, so without the group additions every device open fails with a permission error rather than a missing-device error. Reading the GIDs with `stat` avoids hardcoding values that differ between Pi OS releases.

Add the optional buses when the build includes them:

```bash
--device /dev/i2c-1 --group-add "$(stat -c '%g' /dev/i2c-1)" \
  --device /dev/spidev0.0 --device /dev/spidev0.1 \
  --group-add "$(stat -c '%g' /dev/spidev0.0)" \
```

For a board on `/dev/ttyACM0`, pass the node and tell the application about it: `--device /dev/ttyACM0 -e CHESS_GANTRY_SERIAL_PORT=/dev/ttyACM0`.

To try the stack with no hardware attached, drop every `--device` and `--group-add` flag and add `-e CHESS_GANTRY_DEMO=1`.

## Reaching the dashboard

Binding `0.0.0.0` is the default, so the entrypoint requires a token and generates one when `CHESS_GANTRY_WEB_TOKEN` is unset. Read it from the log:

```bash
docker logs chess-gantry
```

The log opens with a device report, one line per node, marked `rw`, `ro`, `no access` or `missing`. Check that before debugging anything else. The generated token follows.

Then open `http://<pi-ip>:8000/?token=<token>`.

Anyone holding the token can move the gantry. To pin your own instead of reading it from the log, pass `-e CHESS_GANTRY_WEB_TOKEN=...`, and keep it out of shared shell history.

## Debug console

The raw G-code console is a second command, so it needs a second container. One container runs one process.

```bash
docker run -d --name chess-gantry-console --restart unless-stopped \
  --device /dev/ttyUSB0 \
  --group-add "$(stat -c '%g' /dev/ttyUSB0)" \
  --publish 8300:8300 \
  --volume "$PWD/config.json:/app/config.json:ro" \
  --volume "$PWD/data:/app/data" \
  chess:latest debug-console
```

Only one process can hold the serial port at a time. Stop the web container first, or point the console at a different board.

## Environment variables

Set with `-e` on the run command. `.env.example` documents the full set.

| Variable                   | Default        | Purpose                                                               |
| -------------------------- | -------------- | --------------------------------------------------------------------- |
| `CHESS_GANTRY_SERIAL_PORT` | `/dev/ttyUSB0` | Serial device the controller opens.                                   |
| `CHESS_GANTRY_WEB_HOST`    | `0.0.0.0`      | Use `127.0.0.1` to keep the dashboard on loopback and skip the token. |
| `CHESS_GANTRY_WEB_PORT`    | `8000`         | In-container dashboard port.                                          |
| `CHESS_GANTRY_WEB_TOKEN`   | generated      | Dashboard token, printed to the log if unset.                         |
| `CHESS_GANTRY_DEBUG_TOKEN` | generated      | Debug console token.                                                  |
| `CHESS_GANTRY_DEMO`        | `0`            | Simulated hardware, no devices needed.                                |
| `LICHESS_TOKEN`            | empty          | Raises Lichess rate limits and reads own games.                       |
| `TZ`                       | `UTC`          | Container time zone.                                                  |

## Operating

```bash
docker logs -f --tail 200 chess-gantry
docker ps --filter name=chess-gantry
docker inspect --format '{{.State.Health.Status}}' chess-gantry
docker stop chess-gantry && docker rm chess-gantry
```

The image ships a `HEALTHCHECK` that curls the dashboard root every 30 seconds after a 20 second grace period, which is why `Health.Status` is meaningful.

Rebuild and replace after pulling changes:

```bash
git pull --ff-only
git submodule update --init --recursive
docker build --tag chess:latest --build-arg INCLUDE_GPIO=1 .
docker stop chess-gantry && docker rm chess-gantry
```
