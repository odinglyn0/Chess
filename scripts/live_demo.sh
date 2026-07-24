#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

./scripts/demo_check.sh
exec uv run chess-gantry \
  --config config.demo.json \
  --state data/demo/board_state.json \
  --journal data/demo/pending_move.json \
  --audit data/demo/audit.jsonl \
  web --demo
