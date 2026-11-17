import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from temporal_drift.config import load_config
from temporal_drift.data.synthetic import create_fixture
from temporal_drift.pipeline import DEFAULT_STAGES, resolve_stages, run


def test_stage_order_download_before_snapshot():
    stages, _ = resolve_stages(["metrics", "download"])
    assert stages.index("download") < stages.index("inventory") < stages.index("embed")


def test_direct_heavy_pipeline_requires_tmux(tmp_path, monkeypatch):
    cfg = load_config(create_fixture(tmp_path / "fixture"))
    monkeypatch.delenv("TMUX", raising=False)
    with pytest.raises(RuntimeError, match="tmux"):
        run(cfg, "blocked", ["taxonomy"])


def test_complete_pipeline_repeatability_and_real_holdout(tmp_path):
    if not os.environ.get("TMUX"):
        pytest.skip("Fitting tests run inside tmux: bash scripts/checks.sh")
    cfg = load_config(create_fixture(tmp_path / "fixture"))
    first = run(cfg, "one", DEFAULT_STAGES)
    # Different artifact root forces independent computation, not a cache-only repeat.
    cfg["artifact_root"] = str(tmp_path / "independent_artifacts")
    second = run(cfg, "two", DEFAULT_STAGES)
    a, b = [json.loads((p / "run.json").read_text()) for p in (first, second)]
    assert a["status"] == b["status"] == "complete"
    for name in a["stages"]:
        assert a["stages"][name]["outputs"] == b["stages"][name]["outputs"], name
    taxonomy = Path(a["stages"]["taxonomy"]["artifact"])
    metrics = pd.read_csv(Path(a["stages"]["metrics"]["artifact"]) / "master_results.csv")
    assert (metrics[metrics.split == "test"].n_pre == 6).all()
    assert (metrics[metrics.split == "full"].n_pre == 12).all()
    assert set(pd.read_csv(taxonomy / "taxonomy.csv").dd_tier) == {"stable", "slow", "fast"}
    stats = json.loads((Path(a["stages"]["statistics"]["artifact"]) / "tests.json").read_text())
    assert stats["H2/language_level"]["n_languages"] == 6
    # Resume the exact immutable run, verify all output hashes, and keep numeric content.
    run(cfg, "two", DEFAULT_STAGES)


def test_manifest_rejects_changed_config_for_same_run(tmp_path):
    cfg = load_config(create_fixture(tmp_path / "fixture"))
    run(cfg, "fixed", ["inventory"])
    cfg["seed"] += 1
    with pytest.raises(ValueError, match="different code"):
        run(cfg, "fixed", ["inventory"])


def test_inventory_mutation_invalidates_downstream_identity(tmp_path):
    from PIL import Image

    cfg = load_config(create_fixture(tmp_path / "fixture"))
    first = run(cfg, "a", ["inventory"])
    p = next(Path(cfg["data_root"]).rglob("*.png"))
    Image.fromarray(np.zeros((16, 16, 3), dtype=np.uint8)).save(p)
    second = run(cfg, "b", ["inventory"])
    ids = [
        json.loads((p / "run.json").read_text())["stages"]["inventory"]["key"]
        for p in [first, second]
    ]
    assert ids[0] != ids[1]
    with pytest.raises(ValueError, match="Inputs for inventory changed"):
        run(cfg, "a", ["inventory"])
