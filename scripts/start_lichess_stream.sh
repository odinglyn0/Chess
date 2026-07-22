#!/usr/bin/env bash
set -euo pipefail

# The stream service comes from the pinned odinglyn0/Chess submodule.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SERVICE_DIR="$ROOT/services/lichess_stream/services/lichess_stream"

if [[ ! -f "$SERVICE_DIR/pyproject.toml" ]]; then
  printf 'Lichess stream submodule is missing. Run: git submodule update --init --recursive\n' >&2
  exit 1
fi

if command -v docker > /dev/null 2>&1 && docker compose version > /dev/null 2>&1; then
  exec docker compose -f "$ROOT/docker-compose.lichess.yml" up --build
fi

# Docker is optional. Run the upstream FastAPI service locally when unavailable.
VENV="$SERVICE_DIR/.venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  python3 -m venv "$VENV"
  "$VENV/bin/python" -m pip install --upgrade pip
  "$VENV/bin/python" -m pip install "$SERVICE_DIR"
fi

export CHESS_STREAM_HOST="${CHESS_STREAM_HOST:-127.0.0.1}"
export CHESS_STREAM_PORT="${CHESS_STREAM_PORT:-8010}"
export CHESS_STREAM_SCHEMA_PATH="${CHESS_STREAM_SCHEMA_PATH:-$ROOT/schemas/board_state.schema.json}"
exec "$VENV/bin/python" -m chess_stream
