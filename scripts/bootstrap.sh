#!/usr/bin/env bash
# Environment provisioning also survives SSH disconnects.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
mode="${1:-core}"
if [[ "$mode" != core && "$mode" != research ]]; then
  echo "Usage: bash scripts/bootstrap.sh [core|research]" >&2
  exit 2
fi
if [[ -z "${TMUX:-}" ]]; then
  command -v tmux >/dev/null || { echo "Install tmux first." >&2; exit 1; }
  mkdir -p .logs
  session="tdrift-setup-$(date -u +%Y%m%dT%H%M%S)"
  printf -v task 'bash %q %q > %q 2>&1' "$PWD/scripts/bootstrap.sh" "$mode" "$PWD/.logs/$session.log"
  tmux new-session -d -s "$session" -c "$PWD" -e "PATH=$PATH" "$task"
  echo "Session: $session"
  echo "Log: $PWD/.logs/$session.log"
  echo "Attach: tmux attach -t $session"
  exit 0
fi
command -v uv >/dev/null || { echo "Install uv: https://docs.astral.sh/uv/getting-started/installation/" >&2; exit 1; }
if [[ "$mode" == research ]]; then
  uv sync --frozen --extra models --extra viz --extra dev
else
  uv sync --frozen --extra dev
fi
.venv/bin/tdrift validate
echo "Environment ready."
