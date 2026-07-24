#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src uv run python -m compileall -q src tests examples
PYTHONPATH=src uv run python -m unittest discover -s tests -v
