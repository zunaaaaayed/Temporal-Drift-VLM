import json
from pathlib import Path

import numpy as np
from PIL import Image

from temporal_drift.data.inventory import scan_images
from temporal_drift.models.embeddings import extract_visual, load_visual


def test_inventory_rejects_corruption_and_cross_label_duplicates(tmp_path):
    cfg = {
        "data_root": str(tmp_path),
        "experiment": {"concepts": ["phone", "mountain"], "temporal_bins": ["a", "b", "c"]},
    }
    image = Image.fromarray(np.full((8, 8, 3), 20, dtype=np.uint8))
    for concept in ["phone", "mountain"]:
        folder = tmp_path / "images" / concept / "a"
        folder.mkdir(parents=True)
        image.save(folder / "duplicate.png")
    (folder / "corrupt.jpg").write_bytes(b"not an image")
    inventory, rejected = scan_images(cfg)
    assert len(inventory) == 1
    assert inventory.iloc[0].concept == "mountain"
    assert len(rejected) == 2
    assert any(r["reason"] == "duplicate_content" for r in rejected)


def test_visual_extraction_resumes_verified_batches(tmp_path, monkeypatch):
    cfg = {
        "data_root": str(tmp_path),
        "experiment": {
            "concepts": ["phone"],
            "temporal_bins": ["a", "b", "c"],
            "models": {"clip": {}},
        },
        "batch_size": 2,
    }
    folder = tmp_path / "images" / "phone" / "a"
    folder.mkdir(parents=True)
    for i in range(5):
        Image.fromarray(np.full((8, 8, 3), i, dtype=np.uint8)).save(folder / f"{i}.png")
    inventory, _ = scan_images(cfg)
    calls = []

    class Encoder:
        def runtime(self):
            return {"fixture": True}

        def images(self, images):
            calls.append(len(images))
            if len(calls) == 2:
                raise RuntimeError("interrupted")
            return np.array([[image.getpixel((0, 0))[0] + 1, 1.0] for image in images])

    from temporal_drift.models import embeddings

    monkeypatch.setattr(embeddings, "load_encoder", lambda *_: Encoder())
    output = tmp_path / "artifacts"
    output.mkdir()
    import pytest

    with pytest.raises(RuntimeError):
        extract_visual(cfg, output, inventory)
    # One completed batch is reused; only the remaining three images are encoded.
    calls.clear()

    class ResumedEncoder(Encoder):
        def images(self, images):
            calls.append(len(images))
            return np.array([[image.getpixel((0, 0))[0] + 1, 1.0] for image in images])

    monkeypatch.setattr(embeddings, "load_encoder", lambda *_: ResumedEncoder())
    extract_visual(cfg, output, inventory)
    assert sum(calls) == 3
    values, meta = load_visual(output, "clip")
    assert len(values) == len(meta) == 5
    assert meta.image_id.tolist() == inventory.image_id.tolist()
    assert len(list(Path(output).rglob("batch-*.json"))) == 3
    assert json.loads((output / "clip" / "runtime.json").read_text()) == {"fixture": True}
