"""CLI: long-running commands automatically launch in a detached tmux session."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from .config import load_config
from .provenance import now


def configure_process(cfg):
    expected = {
        "PYTHONHASHSEED": str(cfg["seed"]),
        "CUBLAS_WORKSPACE_CONFIG": ":4096:8",
        "OMP_NUM_THREADS": str(cfg["threads"]),
        "OPENBLAS_NUM_THREADS": str(cfg["threads"]),
        "MKL_NUM_THREADS": str(cfg["threads"]),
        "NUMEXPR_NUM_THREADS": str(cfg["threads"]),
        "MPLBACKEND": "Agg",
        "TOKENIZERS_PARALLELISM": "false",
    }
    changed = any(os.environ.get(k) != v for k, v in expected.items())
    os.environ.update(expected)
    # Python hash randomization and BLAS thread limits must be set before interpreter startup.
    if changed:
        os.execv(sys.executable, [sys.executable, "-m", "temporal_drift", *sys.argv[1:]])


def launch_tmux(arguments, cfg, run_id):
    if not shutil.which("tmux"):
        raise RuntimeError("tmux is required for long jobs; install tmux, then repeat this command")
    run_dir = Path(cfg["run_root"]) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    session = f"tdrift-{run_id}"
    if (
        subprocess.run(["tmux", "has-session", "-t", f"={session}"], capture_output=True).returncode
        == 0
    ):
        raise RuntimeError(
            f"Session already exists: {session}; attach with tmux attach -t {session}"
        )
    command = shlex.join([sys.executable, "-m", "temporal_drift", *arguments, "--worker"])
    # exec keeps the pipeline's real exit status. A short shell tail records it even on failure.
    log = shlex.quote(str(run_dir / "console.log"))
    exit_path = shlex.quote(str(run_dir / "exit_code.txt"))
    script = (
        f"{command} >> {log} 2>&1\n"
        f'tdrift_exit=$?\nprintf \'%s\\n\' "$tdrift_exit" > {exit_path}\nexit "$tdrift_exit"'
    )
    # Pass project environment explicitly: a persistent tmux server may have an old PATH/PYTHONPATH.
    env_keys = [
        "PYTHONPATH",
        "PATH",
        "VIRTUAL_ENV",
        "HF_HOME",
        "PYTHONHASHSEED",
        "CUBLAS_WORKSPACE_CONFIG",
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "MPLBACKEND",
        "TOKENIZERS_PARALLELISM",
    ]
    cmd = ["tmux", "new-session", "-d", "-s", session, "-c", str(Path.cwd())]
    for key in env_keys:
        if key in os.environ:
            cmd += ["-e", f"{key}={os.environ[key]}"]
    cmd += [shlex.join(["bash", "-c", script])]
    subprocess.run(cmd, check=True)
    print(
        f"Started tmux session: {session}\nAttach: tmux attach -t {session}\n"
        f"Log: {run_dir / 'console.log'}\nStatus: tdrift status --config {cfg['_config_path']} --run-id {run_id}"
    )


def parser():
    p = argparse.ArgumentParser(description="Reproducible temporal drift experiments")
    sub = p.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Run/resume stages; automatically use tmux")
    run.add_argument("--config", default="configs/research.json")
    run.add_argument("--run-id")
    run.add_argument("--stages", nargs="+")
    run.add_argument("--with-style", action="store_true")
    run.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    status = sub.add_parser("status", help="Read run state without importing model libraries")
    status.add_argument("--config", default="configs/research.json")
    status.add_argument("--run-id", required=True)
    status.add_argument("--json", action="store_true", help="Print the full manifest")
    check = sub.add_parser(
        "validate", help="Validate a configuration without fitting or downloading"
    )
    check.add_argument("--config", default="configs/research.json")
    sub.add_parser("stages", help="List available stages and dependencies")
    smoke = sub.add_parser(
        "smoke", help="Generate a tiny local fixture and launch the pipeline in tmux"
    )
    smoke.add_argument("--root", default="runs/smoke-fixture")
    smoke.add_argument("--run-id", default="smoke")
    compare = sub.add_parser("compare", help="Compare numeric artifact hashes for two runs")
    compare.add_argument("first")
    compare.add_argument("second")
    return p


def main():
    args = parser().parse_args()
    try:
        if args.command == "stages":
            from .pipeline import DEPENDENCIES

            for name, dependencies in DEPENDENCIES.items():
                print(f"{name:14s} <- {', '.join(dependencies) or '(none)'}")
            return
        if args.command == "compare":
            a, b = [
                json.loads((Path(p) / "run.json").read_text()) for p in (args.first, args.second)
            ]
            if a["status"] != "complete" or b["status"] != "complete":
                raise ValueError("Both runs must be complete")
            equal = True
            from .artifacts import verify

            for name in sorted(set(a["stages"]) | set(b["stages"])):
                left, right = a["stages"].get(name), b["stages"].get(name)
                if left:
                    verify(Path(left["artifact"]))
                if right:
                    verify(Path(right["artifact"]))
                matches = bool(left and right and left["outputs"] == right["outputs"])
                equal &= matches
                print(f"{name}: {'identical' if matches else 'DIFFERENT'}")
            if not equal:
                raise SystemExit(1)
            return
        if args.command == "smoke":
            from .data.synthetic import create_fixture

            config = create_fixture(Path(args.root).resolve())
            os.execv(
                sys.executable,
                [
                    sys.executable,
                    "-m",
                    "temporal_drift",
                    "run",
                    "--config",
                    str(config),
                    "--run-id",
                    args.run_id,
                ],
            )
        cfg = load_config(args.config)
        if args.command == "validate":
            print(
                f"Valid configuration: {args.config}\nConcepts: {len(cfg['experiment']['concepts'])}"
                f"\nSynthetic: {cfg['synthetic']}\nModel/dataset revisions: immutable"
            )
            return
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", args.run_id or "run"):
            raise ValueError("run-id must contain only letters, digits, underscores, and hyphens")
        if args.command == "status":
            folder = Path(cfg["run_root"]) / args.run_id
            manifest = folder / "run.json"
            if not manifest.exists():
                print("Run has not started yet")
            elif args.json:
                print(manifest.read_text())
            else:
                record = json.loads(manifest.read_text())
                print(f"Run: {args.run_id} | {record['status']} | synthetic={record['synthetic']}")
                for name, stage in record["stages"].items():
                    print(f"  {name:14s} {stage['status']:10s} {stage.get('artifact', '')}")
                if record.get("error"):
                    print("Error:", record["error"])
            if (folder / "exit_code.txt").exists():
                print("Exit code:", (folder / "exit_code.txt").read_text().strip())
            return
        configure_process(cfg)
        run_id = args.run_id or now().replace(":", "").replace("-", "").replace("+", "_").replace(
            ".", "_"
        )
        arguments = ["run", "--config", str(Path(args.config).resolve()), "--run-id", run_id]
        if args.stages:
            arguments += ["--stages", *args.stages]
        if args.with_style:
            arguments += ["--with-style"]
        if not os.environ.get("TMUX"):
            if args.worker:
                raise ValueError("Workers must run inside tmux")
            launch_tmux(arguments, cfg, run_id)
            return
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
        from .pipeline import DEFAULT_STAGES, run

        run(cfg, run_id, args.stages or DEFAULT_STAGES, with_style=args.with_style)
    except (ValueError, RuntimeError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
