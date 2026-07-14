#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -e .

if [[ ! -e config.json ]]; then
  cp config.example.json config.json
fi
mkdir -p data
if [[ ! -e data/board_state.json ]]; then
  cp examples/board_state.standard.json data/board_state.json
fi

cat <<'EOF'
Installed.
Next:
  source .venv/bin/activate
  chess-gantry --config config.json ports
  chess-gantry --config config.json plan examples/move_e2_e4.json

Hardware execution remains locked until you calibrate config.json and set
safety.calibrated to true.
EOF
