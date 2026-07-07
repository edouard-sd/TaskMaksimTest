#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

export PYTHONPATH="packages/schemas${PYTHONPATH:+:$PYTHONPATH}"

echo "== Smoke test: sample workflows =="
python scripts/smoke_test_workflows.py

echo
echo "== Automated tests =="
python -m pytest
