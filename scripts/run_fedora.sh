#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  ./scripts/install_pi.sh
fi

if [[ ! -f config.json ]]; then
  cp config.example.json config.json
fi
mkdir -p data
if [[ ! -f data/board_state.json ]]; then
  cp examples/board_state.standard.json data/board_state.json
fi

MOVE_JSON="${1:-examples/move_e2_e4.json}"
if [[ $# -gt 0 && "$1" == *.json ]]; then
  shift
fi

exec uv run chess-gantry \
  --config config.json \
  --state data/board_state.json \
  --journal data/pending_move.json \
  --audit data/audit.jsonl \
  run "$MOVE_JSON" "$@"
