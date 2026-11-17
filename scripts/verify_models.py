"""Explicit real-weight integration check; invoke inside tmux on a compute host.

Example: tmux new-session -s adapters '.venv/bin/python scripts/verify_models.py'
Weights are large. This is deliberately separate from the offline test suite.
"""

import json
import os
from pathlib import Path

if not os.environ.get("TMUX"):
    raise SystemExit("Run this model inference check inside tmux; see this script's docstring.")

# Configure numerical backends before importing NumPy/torch.
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[key] = "1"
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from temporal_drift.config import load_config  # noqa: E402
from temporal_drift.models.encoders import load_encoder  # noqa: E402
from temporal_drift.provenance import atomic_json, file_hash  # noqa: E402

cfg = load_config("configs/research.json")
cfg["device"] = "cpu"
image = Image.fromarray(np.random.default_rng(42).integers(0, 256, (256, 256, 3), dtype=np.uint8))
output = Path("runs/model-adapter-check")
output.mkdir(parents=True, exist_ok=True)
results = {}
for key in cfg["experiment"]["models"]:
    encoder = load_encoder(cfg, key)
    visual = encoder.images([image])
    text = encoder.texts(["A photograph of a phone.", "একটি ফোন এর ছবি।", "電話の写真。"])
    np.testing.assert_array_equal(visual, encoder.images([image]))
    np.testing.assert_array_equal(
        text, encoder.texts(["A photograph of a phone.", "একটি ফোন এর ছবি।", "電話の写真。"])
    )
    assert visual.shape[1] == text.shape[1] == cfg["experiment"]["models"][key]["embedding_dim"]
    np.testing.assert_allclose(np.linalg.norm(visual, axis=1), 1, atol=1e-5)
    np.testing.assert_allclose(np.linalg.norm(text, axis=1), 1, atol=1e-5)
    results[key] = {
        "image_shape": list(visual.shape),
        "text_shape": list(text.shape),
        "runtime": encoder.runtime(),
        "sources": cfg["sources"],
    }
    atomic_json(output / "results.json", results)
    print(json.dumps(results[key]), flush=True)
    del encoder
atomic_json(output / "verified.json", {"results_sha256": file_hash(output / "results.json")})
