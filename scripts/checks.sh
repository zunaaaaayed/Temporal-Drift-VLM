#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
if [[ -z "${TMUX:-}" ]]; then
  mkdir -p .logs
  session="tdrift-checks-$(date -u +%Y%m%dT%H%M%S)"
  printf -v task 'bash %q > %q 2>&1' "$PWD/scripts/checks.sh" "$PWD/.logs/$session.log"
  tmux new-session -d -s "$session" -c "$PWD" -e "PATH=$PATH" "$task"
  echo "Session: $session"
  echo "Log: $PWD/.logs/$session.log"
  exit 0
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONHASHSEED=42
export MPLBACKEND=Agg
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
.venv/bin/ruff check src tests scripts
.venv/bin/python -m pytest -q
