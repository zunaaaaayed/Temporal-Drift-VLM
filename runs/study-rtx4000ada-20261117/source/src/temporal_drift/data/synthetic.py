"""Offline end-to-end fixture, deliberately distinct from research results."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image

from ..provenance import atomic_json


def create_fixture(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    repo = Path(__file__).resolve().parents[3]
    original = repo / "configs"
    if not original.exists():
        raise FileNotFoundError("Smoke fixture requires the repository checkout")
    cfg = json.loads((original / "research.json").read_text())
    experiment = json.loads((original / "experiment.notebook.json").read_text())
    experiment["concepts"] = ["mountain", "river", "hospital", "office", "phone", "television"]
    experiment["concept_tiers"] = {
        "stable": ["mountain", "river"],
        "slow": ["hospital", "office"],
        "fast": ["phone", "television"],
    }
    experiment.update(n_proj_swd=12, n_permutations=20, k_values=[10, 50])
    for key in ["prompts", "sources"]:
        atomic_json(root / f"{key}.json", json.loads((original / cfg[key]).read_text()))
        cfg[key] = f"{key}.json"
    atomic_json(root / "experiment.json", experiment)
    cfg.update(
        experiment="experiment.json",
        data_root="data",
        artifact_root="artifacts",
        run_root="runs",
        synthetic=True,
        synthetic_dimension=16,
        device="cpu",
        batch_size=12,
        statistical_permutations=50,
        compute_icc=False,
        grids=[["phone", "en", "clip"]],
    )
    for i, concept in enumerate(experiment["concepts"]):
        for j, b in enumerate(experiment["temporal_bins"]):
            for k in range(12):
                dest = root / "data" / "images" / concept / b / f"{k:03d}.png"
                if dest.exists():
                    continue
                rng = np.random.default_rng(42 + i * 1000 + j * 100 + k)
                pixels = rng.integers(0, 80, size=(16, 16, 3), dtype=np.uint8)
                pixels[..., i % 3] += np.uint8(60 + j * (5 + i * 3))
                dest.parent.mkdir(parents=True, exist_ok=True)
                Image.fromarray(pixels).save(dest)
    atomic_json(root / "smoke.json", cfg)
    return root / "smoke.json"
