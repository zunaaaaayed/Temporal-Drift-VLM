"""Content-addressed stage outputs with integrity checks and exclusive locks."""

from __future__ import annotations

import fcntl
import json
from contextlib import contextmanager
from pathlib import Path

from .provenance import atomic_json, digest, file_hash, now


@contextmanager
def exclusive_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def output_hashes(folder: Path) -> dict:
    return {
        p.relative_to(folder).as_posix(): file_hash(p)
        for p in sorted(folder.rglob("*"))
        if p.is_file() and p.name != "_complete.json" and not p.name.startswith(".")
    }


def verify(folder: Path) -> dict:
    record = json.loads((folder / "_complete.json").read_text())
    if output_hashes(folder) != record["outputs"]:
        raise ValueError(
            f"Artifact integrity failure: {folder}. Preserve it and use a new artifact root."
        )
    return record


def build(root: Path, stage: str, identity: dict, function) -> tuple[Path, dict]:
    key = digest(identity)
    folder = root / stage / key
    with exclusive_lock(root / ".locks" / f"{stage}-{key}.lock"):
        if (folder / "_complete.json").exists():
            return folder, verify(folder)
        folder.mkdir(parents=True, exist_ok=True)
        function(folder)
        record = {
            "schema": 1,
            "stage": stage,
            "key": key,
            "identity": identity,
            "completed_at": now(),
            "outputs": output_hashes(folder),
        }
        atomic_json(folder / "_complete.json", record)
        return folder, record
