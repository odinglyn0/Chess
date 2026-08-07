# Docker

Build and run the `chess:latest` image on a Raspberry Pi, with GPIO and the Marlin serial link passed through and the web dashboard published on the LAN.

The runtime stage is built `FROM scratch`, so the image has no shell. Everything below uses `docker logs`, `docker inspect` and rebuilds instead of `docker exec ... bash`.

## Requirements

- 64-bit Raspberry Pi OS. The image is Fedora-based and Fedora publishes no 32-bit armhf builds, so a 32-bit Pi OS install cannot run it.
- Docker Engine with the Compose plugin: `./scripts/install_pi.sh` installs both.
- I2C and SPI enabled in `/boot/firmware/config.txt` (`dtparam=i2c_arm=on`, `dtparam=spi=on`) followed by a reboot, but only if the build uses those buses. Without it the `/dev/i2c-*` and `/dev/spidev*` nodes do not exist.

Build on the Pi itself. Cross-building from an x86_64 host produces an amd64 image that will not start on ARM.

## Quick start

`./scripts/run_docker.sh` builds the image and serves it in one step. Paste a Clerk development publishable key into the `CLERK_PUBLISHABLE_KEY` line near the top of the script first, or export it.

```bash
./scripts/run_docker.sh
```

It builds `chess:latest`, seeds `config.json` and `data/` if they are missing, makes the dashboard answer to `chess.local`, and runs the container in the foreground so Control-C stops it. When `/dev/ttyUSB0` is absent it starts in demo mode with a simulated controller instead of failing.

The dashboard lands on host port 80 and port 8000, so `http://chess.local` and `http://chess.local:8000` both work.

For `chess.local` to resolve, the script uses whichever applies:

- The host is already named `chess`, so avahi answers for it.
- Otherwise it runs `avahi-publish` to advertise a `chess.local` alias for the LAN address, for as long as the script runs. Install it with `sudo apt-get install -y avahi-daemon avahi-utils`.

It never renames the host. To make the name permanent instead, run `sudo hostnamectl set-hostname chess` once and drop avahi-utils.

Overrides, all optional:

| Variable                   | Default        | Effect                                               |
| -------------------------- | -------------- | ---------------------------------------------------- |
| `CHESS_GANTRY_HTTP_PORT`   | `80`           | Primary host port. Use `8080` if 80 is taken.        |
| `CHESS_GANTRY_ALT_PORT`    | `8000`         | Second host port, skipped when it matches the first. |
| `CHESS_GANTRY_MDNS_NAME`   | `chess.local`  | Advertised name and the URL that gets printed.       |
| `CHESS_GANTRY_SERIAL_PORT` | `/dev/ttyUSB0` | Serial device to attach.                             |

The rest of this document covers the manual build and run for anything the script does not fit.

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

The dashboard binds every interface and authenticates with Clerk. Open `http://chess.local` or `http://<pi-ip>:8000/` and sign in. There is no token and no URL to keep secret.

```bash
docker logs chess-gantry
```

The log opens with a device report, one line per node, marked `rw`, `ro`, `no access` or `missing`. Check that before debugging anything else.

Anyone who can route to the host reaches the sign-in page, including the public internet once you forward the port or run a tunnel. Access is exactly the set of people who can sign in to your Clerk instance, so control that in the Clerk dashboard.

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

| Variable                   | Default        | Purpose                                                      |
| -------------------------- | -------------- | ------------------------------------------------------------ |
| `CHESS_GANTRY_SERIAL_PORT` | `/dev/ttyUSB0` | Serial device the controller opens.                          |
| `CLERK_PUBLISHABLE_KEY`    | empty          | Required. Without it the dashboard refuses to start.         |
| `CLERK_SECRET_KEY`         | empty          | Accepted for completeness, unused by session checks.         |
| `CHESS_GANTRY_WEB_HOST`    | `0.0.0.0`      | Every interface. Use `127.0.0.1` to restrict it to the host. |
| `CHESS_GANTRY_WEB_PORT`    | `8000`         | In-container dashboard port.                                 |
| `CHESS_GANTRY_PUBLIC_HOST` | empty          | Hostname printed in the startup URL, e.g. `chess.local`.     |
| `CHESS_GANTRY_DEBUG_TOKEN` | generated      | Debug console token. Separate app, unchanged.                |
| `CHESS_GANTRY_DEMO`        | `0`            | Simulated hardware, no devices needed.                       |
| `LICHESS_TOKEN`            | empty          | Raises Lichess rate limits and reads own games.              |
| `TZ`                       | `UTC`          | Container time zone.                                         |

## Clerk sign-in

Clerk is the only authentication the dashboard has. `CLERK_PUBLISHABLE_KEY` is required and the server exits with a clear error when it is missing. Nothing else needs configuring: the frontend API host, the JWT issuer and the JWKS URL are all decoded from the publishable key.

```bash
docker run -d --name chess-gantry --restart unless-stopped \
  --device /dev/ttyUSB0 \
  --group-add "$(stat -c '%g' /dev/ttyUSB0)" \
  --publish 8000:8000 \
  --volume "$PWD/config.json:/app/config.json:ro" \
  --volume "$PWD/data:/app/data" \
  -e CLERK_PUBLISHABLE_KEY=pk_test_dGhhbmtmdWwtcmF5LTU4LmNsZXJrLmFjY291bnRzLmRldiQ \
  chess:latest
```

How it works: `GET /` is public because it has to serve the sign-in page. Clerk's JS runs sign-in and maintains the `__session` cookie on the dashboard origin. Every `/api/*` route reads that cookie and verifies it as an RS256 JWT against the instance JWKS, checking the issuer and requiring `exp`, `iat` and `sub`. No bearer headers, no shared secret, nothing to copy around.

Because the cookie alone authorises requests, state-changing requests arriving with `Sec-Fetch-Site: cross-site` are refused, which stops another site from driving the gantry through a signed-in browser.

Anyone who can sign in to your Clerk instance can move the gantry. Clerk allows open sign-ups by default, so set whatever restrictions you want in the Clerk dashboard.

One deployment caveat: a `pk_live_` production instance requires HTTPS, so its `__session` cookie carries `Secure` and will not be sent over plain `http://<ip>:8000`. Use a `pk_test_` development instance for plain-HTTP access, or put the dashboard behind TLS.

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
