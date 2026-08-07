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

if ! sudo docker compose version > /dev/null 2>&1; then
  printf 'Installing the Docker Compose plugin...\n'
  sudo apt-get update
  sudo apt-get install -y docker-compose-plugin
fi

sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
sudo usermod -aG dialout "$USER"

if [[ ! -f config.json ]]; then
  cp config.example.json config.json
fi

mkdir -p data
if [[ ! -f data/board_state.json ]]; then
  cp examples/board_state.standard.json data/board_state.json
fi

SERIAL_DEVICE="${CHESS_GANTRY_SERIAL_DEVICE:-/dev/ttyUSB0}"
PORT="${CHESS_GANTRY_WEB_PORT:-8000}"

if [[ -z "${CLERK_PUBLISHABLE_KEY:-}" ]]; then
  printf 'CLERK_PUBLISHABLE_KEY is not set. The dashboard authenticates with Clerk only.\n' >&2
  printf 'Export it before running this installer.\n' >&2
  exit 2
fi

cat > .env.docker << EOF
CHESS_GANTRY_WEB_PORT=$PORT
CHESS_GANTRY_SERIAL_DEVICE=$SERIAL_DEVICE
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

if [[ -e "$SERIAL_DEVICE" ]]; then
  compose up -d
else
  printf 'Serial device %s is not connected, so the image was built but the service was not started.\n' "$SERIAL_DEVICE"
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
