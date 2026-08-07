#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ "$(uname -s)" != "Linux" ]]; then
  printf 'This installer requires Raspberry Pi OS or another Linux system.\n' >&2
  exit 2
fi

if ! command -v sudo > /dev/null 2>&1; then
  printf 'sudo is required to install and configure Docker.\n' >&2
  exit 2
fi

ARCH="$(uname -m)"
case "$ARCH" in
  aarch64 | armv7l | armv8l) ;;

  *)
    printf 'Warning: expected a Raspberry Pi ARM architecture, found %s.\n' "$ARCH"
    ;;
esac

if ! command -v docker > /dev/null 2>&1 || ! docker compose version > /dev/null 2>&1; then
  printf 'Installing Docker Engine and the Compose plugin...\n'
  sudo apt-get update
  sudo apt-get install -y ca-certificates curl
  INSTALLER="$(mktemp)"
  trap 'rm -f "$INSTALLER"' EXIT
  curl -fsSL https://get.docker.com -o "$INSTALLER"
  sudo sh "$INSTALLER"
  rm -f "$INSTALLER"
  trap - EXIT
fi

sudo apt-get update
sudo apt-get install -y i2c-tools

BOOT_CONFIG=/boot/firmware/config.txt
if [[ ! -f $BOOT_CONFIG ]]; then
  BOOT_CONFIG=/boot/config.txt
fi
I2C_REBOOT_REQUIRED=0
if [[ -f $BOOT_CONFIG ]] && ! grep -qE '^dtparam=i2c_arm=on([[:space:]]|$)' "$BOOT_CONFIG"; then
  printf '\n# Chess Gantry MCP23017\ndtparam=i2c_arm=on\n' | sudo tee -a "$BOOT_CONFIG" > /dev/null
  printf 'Enabled Raspberry Pi I2C in %s. Reboot before starting the reed switch test.\n' "$BOOT_CONFIG"
  I2C_REBOOT_REQUIRED=1
fi

if ! sudo docker compose version > /dev/null 2>&1; then
  printf 'Installing the Docker Compose plugin...\n'
  sudo apt-get update
  sudo apt-get install -y docker-compose-plugin
fi

sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
sudo usermod -aG dialout "$USER"

if [[ $I2C_REBOOT_REQUIRED -eq 1 ]]; then
  printf 'Reboot now, then rerun ./scripts/install_pi.sh to build and start the container.\n'
  exit 0
fi

if [[ ! -f config.json ]]; then
  cp config.example.json config.json
fi

mkdir -p data
if [[ ! -f data/board_state.json ]]; then
  cp examples/board_state.standard.json data/board_state.json
fi

SERIAL_DEVICE="${CHESS_GANTRY_SERIAL_DEVICE:-/dev/ttyUSB0}"
I2C_DEVICE="${CHESS_GANTRY_I2C_DEVICE:-/dev/i2c-1}"
PORT="${CHESS_GANTRY_WEB_PORT:-8000}"

if [[ -z "${CLERK_PUBLISHABLE_KEY:-}" ]]; then
  printf 'CLERK_PUBLISHABLE_KEY is not set. The dashboard authenticates with Clerk only.\n' >&2
  printf 'Export it before running this installer.\n' >&2
  exit 2
fi

cat > .env.docker << EOF
CHESS_GANTRY_WEB_PORT=$PORT
CHESS_GANTRY_SERIAL_DEVICE=$SERIAL_DEVICE
CHESS_GANTRY_I2C_DEVICE=$I2C_DEVICE
CHESS_GANTRY_I2C_BUS=1
CHESS_GANTRY_MCP23017_ADDRESS=0x20
CLERK_PUBLISHABLE_KEY=$CLERK_PUBLISHABLE_KEY
CLERK_SECRET_KEY=${CLERK_SECRET_KEY:-}
EOF
chmod 600 .env.docker

DOCKER=(docker)
if ! docker info > /dev/null 2>&1; then
  DOCKER=(sudo docker)
fi

compose() {
  "${DOCKER[@]}" compose --env-file .env.docker -f docker-compose.pi.yml "$@"
}

printf 'Building the Chess Gantry container for %s. This can take several minutes on a Pi 3B+.\n' "$ARCH"
compose build

if [[ -e "$SERIAL_DEVICE" && -e "$I2C_DEVICE" ]]; then
  compose up -d
else
  printf 'Required devices are missing, so the image was built but the service was not started.\n'
  printf '  serial: %s\n  I2C: %s\n' "$SERIAL_DEVICE" "$I2C_DEVICE"
fi

LAN_IP="$(hostname -I 2> /dev/null | awk '{print $1}')"
LAN_IP="${LAN_IP:-RASPBERRY_PI_IP}"

cat << EOF

Chess Gantry Docker installation complete.

Dashboard URL, open to everyone who can route here, Clerk sign-in required:
  http://$LAN_IP:$PORT/

Management commands:
  ./scripts/pi_docker.sh status
  ./scripts/pi_docker.sh logs
  ./scripts/pi_docker.sh test
  ./scripts/pi_docker.sh restart
  ./scripts/pi_docker.sh update
  ./scripts/pi_docker.sh down

If the service was not started, connect the Ender controller and run:
  ./scripts/pi_docker.sh up

The current user was added to the docker and dialout groups. Log out and back in
before using Docker without sudo. Keep .env.docker private; it holds the Clerk keys.
EOF
