#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export CHESS_GANTRY_WEB_TOKEN="${CHESS_GANTRY_WEB_TOKEN:-$(uv run python -c 'import secrets; print(secrets.token_urlsafe(32))')}"
PORT="${CHESS_GANTRY_WEB_PORT:-8000}"

printf 'Starting authenticated Chess Gantry UI on the local network.\n'
printf 'Access token: %s\n' "$CHESS_GANTRY_WEB_TOKEN"
printf 'Keep the printed authenticated URL private.\n'

exec uv run chess-gantry --config config.json web \
  --host 0.0.0.0 \
  --web-port "$PORT" \
  --allow-network \
  --no-browser
