#!/usr/bin/env bash
set -uo pipefail
cd /net/cremi/mdzislam/espaces/travail/Temporal-Drift-VLM
export HF_HOME="$PWD/.models/huggingface" TORCH_HOME="$PWD/.models/torch"
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
.venv/bin/tdrift run --config configs/rtx4000ada-20261117.json --run-id study-rtx4000ada-20261117-text --stages text > runs/study-rtx4000ada-20261117-text/console.log 2>&1
result=$?
printf '%s\n' "$result" > runs/study-rtx4000ada-20261117-text/exit_code.txt
exit "$result"
