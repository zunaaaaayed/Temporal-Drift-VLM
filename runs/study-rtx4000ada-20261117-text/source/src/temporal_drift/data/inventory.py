from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from PIL import Image

from ..provenance import atomic_bytes, file_hash


def scan_images(cfg: dict) -> tuple[pd.DataFrame, list[dict]]:
    """Hash original bytes each run; never infer identity from row numbers or mtimes."""
    root = Path(cfg["data_root"])
    rows, rejected = [], []
    seen = {}
    for concept in sorted(cfg["experiment"]["concepts"]):
        for b in cfg["experiment"]["temporal_bins"]:
            for p in sorted((root / "images" / concept / b).glob("*")):
                if not p.is_file() or p.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                    continue
                rel = p.relative_to(root).as_posix()
                try:
                    with Image.open(p) as image:
                        image.verify()
                    sha = file_hash(p)
                except Exception as exc:
                    rejected.append({"path": rel, "reason": str(exc)})
                    continue
                if sha in seen:
                    rejected.append(
                        {"path": rel, "reason": "duplicate_content", "first_path": seen[sha]}
                    )
                    continue
                seen[sha] = rel
                rows.append(
                    {
                        "image_id": sha,
                        "sha256": sha,
                        "concept": concept,
                        "temp_bin": b,
                        "path": rel,
                        "bytes": p.stat().st_size,
                    }
                )
    columns = ["image_id", "sha256", "concept", "temp_bin", "path", "bytes"]
    frame = pd.DataFrame(rows, columns=columns).sort_values("image_id").reset_index(drop=True)
    if frame.empty:
        raise ValueError(
            f"No readable images in {root / 'images'}; import data or run collect/download"
        )
    return frame, rejected


def write_inventory(folder: Path, frame: pd.DataFrame, rejected: list[dict]) -> None:
    atomic_bytes(folder / "images.csv", frame.to_csv(index=False, lineterminator="\n").encode())
    atomic_bytes(folder / "rejected.json", (json.dumps(rejected, indent=2) + "\n").encode())


def check_image(root: Path, row) -> Image.Image:
    path = root / row.path
    if file_hash(path) != row.sha256:
        raise ValueError(f"Image changed after inventory: {path}")
    with Image.open(path) as image:
        return image.convert("RGB")
