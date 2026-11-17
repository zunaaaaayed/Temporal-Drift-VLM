from __future__ import annotations

import io
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ..data.inventory import check_image
from ..provenance import atomic_bytes, atomic_json, digest, file_hash
from .encoders import load_encoder
from .prompts import build_prompts


def save_array(path, values):
    buffer = io.BytesIO()
    np.save(buffer, values, allow_pickle=False)
    atomic_bytes(Path(path), buffer.getvalue())


def extract_visual(cfg, folder, inventory, *, transform=None):
    """Per-model, per-batch atomic checkpoints survive process failure."""
    for key in cfg["experiment"]["models"]:
        model_dir = folder / key
        model_dir.mkdir(exist_ok=True)
        model = None
        chunks = []
        for start in range(0, len(inventory), cfg["batch_size"]):
            batch = inventory.iloc[start : start + cfg["batch_size"]]
            identity = digest(batch[["image_id", "sha256"]].to_dict("records"))
            checkpoint = model_dir / f"batch-{start:08d}-{identity[:12]}.npy"
            checksum = checkpoint.with_suffix(".json")
            if checkpoint.exists() and checksum.exists():
                if file_hash(checkpoint) != json.loads(checksum.read_text())["sha256"]:
                    raise ValueError(f"Checkpoint corrupted: {checkpoint}")
                values = np.load(checkpoint, allow_pickle=False)
            else:
                if model is None:
                    model = load_encoder(cfg, key)
                    atomic_json(model_dir / "runtime.json", model.runtime())
                images = [check_image(Path(cfg["data_root"]), row) for row in batch.itertuples()]
                if transform:
                    images = [transform(image) for image in images]
                values = model.images(images)
                save_array(checkpoint, values)
                atomic_json(checksum, {"sha256": file_hash(checkpoint), "batch_identity": identity})
            if values.ndim != 2 or not np.isfinite(values).all() or len(values) != len(batch):
                raise ValueError("Checkpoint/metadata length mismatch")
            chunks.append(values)
            print(f"{key}: {start + len(batch)}/{len(inventory)} images", flush=True)
        save_array(model_dir / "visual.npy", np.vstack(chunks))
        atomic_bytes(model_dir / "metadata.csv", inventory.to_csv(index=False).encode())
        del model


def extract_text(cfg, folder):
    prompts = build_prompts(cfg)
    pd.DataFrame(prompts).to_csv(folder / "prompts.csv", index=False)
    for key in cfg["experiment"]["models"]:
        model = load_encoder(cfg, key)
        values = []
        for start in range(0, len(prompts), cfg["batch_size"]):
            values.append(
                model.texts([r["text"] for r in prompts[start : start + cfg["batch_size"]]])
            )
        save_array(folder / f"{key}.npy", np.vstack(values))
        atomic_json(folder / f"{key}.runtime.json", model.runtime())
        del model


def load_visual(folder, model):
    meta = pd.read_csv(folder / model / "metadata.csv")
    values = np.load(folder / model / "visual.npy", allow_pickle=False)
    if len(values) != len(meta) or not meta.image_id.is_unique:
        raise ValueError("Embedding metadata must be unique and aligned")
    return values, meta


def load_text(folder, model):
    return np.load(folder / f"{model}.npy", allow_pickle=False), pd.read_csv(folder / "prompts.csv")
