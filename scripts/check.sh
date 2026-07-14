#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m compileall -q src tests examples
PYTHONPATH=src python -m unittest discover -s tests -v
