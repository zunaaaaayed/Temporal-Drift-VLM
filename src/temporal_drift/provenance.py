"""Stable identities, atomic persistence, and process-level reproducibility."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import random
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def canonical(value) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def task_seed(seed: int, *parts: str) -> int:
    return int(digest([seed, *parts])[:8], 16)


def atomic_json(path: Path, value) -> None:
    atomic_bytes(path, canonical(value) + b"\n")


def atomic_bytes(path: Path, payload: bytes) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_fingerprint() -> str:
    root = Path(__file__).parent
    files = {p.relative_to(root).as_posix(): file_hash(p) for p in sorted(root.rglob("*.py"))}
    repo = root.parents[1]
    for name in ("uv.lock", "pyproject.toml"):
        if (repo / name).exists():
            files[name] = file_hash(repo / name)
    return digest(files)


def snapshot_source(destination: Path) -> dict:
    """Archive dirty working source too, so hashes are not the only recovery record."""
    root = Path(__file__).parent
    files = {
        Path("src/temporal_drift") / p.relative_to(root): p for p in sorted(root.rglob("*.py"))
    }
    repo = root.parents[1]
    for name in ("uv.lock", "pyproject.toml", ".python-version"):
        if (repo / name).exists():
            files[Path(name)] = repo / name
    checksums = {}
    for relative, original in files.items():
        atomic_bytes(destination / relative, original.read_bytes())
        checksums[relative.as_posix()] = file_hash(original)
    atomic_json(destination / "SHA256.json", checksums)
    return checksums


def environment() -> dict:
    packages = sorted(
        (d.metadata["Name"], d.version)
        for d in importlib.metadata.distributions()
        if d.metadata["Name"]
    )
    try:
        gpu = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        ).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        gpu = "unavailable"
    try:
        repo = Path(__file__).resolve().parents[2]
        git_head = subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        git_status = subprocess.check_output(
            ["git", "-C", str(repo), "status", "--porcelain"], text=True
        )
    except (OSError, subprocess.CalledProcessError):
        git_head, git_status = None, None
    cpu = {}
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text().split("\n\n", 1)[0].splitlines():
            key, separator, value = line.partition(":")
            if separator and key.strip() in {"vendor_id", "model name", "flags", "Features"}:
                cpu[key.strip()] = value.strip()
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu": cpu,
        "gpu": gpu,
        "packages": packages,
        "git_head": git_head,
        "git_status": git_status,
        "thread_settings": {
            k: os.environ.get(k)
            for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
        },
    }


def seed_process(seed: int, *, torch_required: bool = False) -> None:
    import numpy as np

    random.seed(seed)
    np.random.seed(seed)
    if torch_required:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        torch.use_deterministic_algorithms(True)
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        torch.set_float32_matmul_precision("highest")
