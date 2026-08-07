#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -z "${CLERK_PUBLISHABLE_KEY:-}" ]]; then
  printf 'CLERK_PUBLISHABLE_KEY is not set. The dashboard authenticates with Clerk only.\n' >&2
  exit 2
fi

PORT="${CHESS_GANTRY_WEB_PORT:-8000}"

printf 'Starting the Chess Gantry UI on every interface, port %s.\n' "$PORT"
printf 'Anyone who can route to this host reaches the sign-in page.\n'

exec uv run chess-gantry --config config.json web \
  --host 0.0.0.0 \
  --web-port "$PORT" \
  --no-browser
