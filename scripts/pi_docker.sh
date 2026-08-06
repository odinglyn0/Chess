#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ENV_FILE="${CHESS_GANTRY_DOCKER_ENV:-.env.docker}"
COMPOSE_FILE="docker-compose.pi.yml"

if [[ ! -f "$ENV_FILE" ]]; then
  printf 'Missing %s. Run ./scripts/install_pi.sh first.\n' "$ENV_FILE" >&2
  exit 2
fi

if docker info > /dev/null 2>&1; then
  DOCKER=(docker)
elif sudo -n docker info > /dev/null 2>&1; then
  DOCKER=(sudo docker)
else
  printf 'Docker is unavailable. Run ./scripts/install_pi.sh first or log out/in after Docker group setup.\n' >&2
  exit 2
fi

compose() {
  "${DOCKER[@]}" compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" "$@"
}

ACTION="${1:-status}"
case "$ACTION" in
  up)
    compose up -d
    ;;
  down)
    compose down
    ;;
  restart)
    compose restart
    ;;
  build)
    compose build
    ;;
  rebuild)
    compose build --pull
    compose up -d --force-recreate
    ;;
  update)
    if [[ -n "$(git status --porcelain)" ]]; then
      printf 'Refusing update because the Pi checkout has local changes. Commit, stash, or discard them first.\n' >&2
      exit 2
    fi
    git pull --ff-only
    git submodule update --init --recursive
    compose build --pull
    compose up -d --force-recreate
    compose ps
    ;;
  logs)
    compose logs -f --tail=200
    ;;
  status)
    compose ps
    ;;
  test)
    "${DOCKER[@]}" build --target test -f Dockerfile .
    ;;
  check)
    printf 'Formatting and Git hygiene require the development checkout. Run npm run check on a development machine or in CI.\n'
    ;;
  firmware-check)
    compose exec chess-gantry python scripts/check_firmware.py
    ;;
  shell)
    printf 'The distroless runtime intentionally has no shell. Use logs, firmware-check, or rebuild instead.\n'
    ;;
  *)
    printf 'Usage: %s {up|down|restart|build|rebuild|update|logs|status|test|check|firmware-check|shell}\n' "$0" >&2
    exit 2
    ;;
esac
