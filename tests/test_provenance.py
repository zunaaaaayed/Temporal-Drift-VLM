import json

import pandas as pd
import pytest

from temporal_drift.artifacts import build, verify
from temporal_drift.analysis.taxonomy import make_splits
from temporal_drift.provenance import atomic_json, digest, task_seed


def test_cache_reuse_invalidation_and_corruption_detection(tmp_path):
    calls = []

    def work(folder):
        calls.append(1)
        atomic_json(folder / "numbers.json", {"result": 3})

    first, _ = build(tmp_path, "test", {"input": "a"}, work)
    second, _ = build(tmp_path, "test", {"input": "a"}, work)
    assert first == second and len(calls) == 1
    third, _ = build(tmp_path, "test", {"input": "b"}, work)
    assert third != first and len(calls) == 2
    atomic_json(first / "numbers.json", {"result": 4})
    with pytest.raises(ValueError, match="integrity"):
        verify(first)


def test_split_uses_ids_and_handles_sparse_bins():
    cfg = {
        "seed": 42,
        "experiment": {"concepts": ["phone"], "temporal_bins": ["a", "b", "c"]},
        "split": {"minimum_per_bin": 4, "label_fraction": 0.5},
    }
    frame = pd.DataFrame(
        [
            {"image_id": f"{b}-{i}", "concept": "phone", "temp_bin": b}
            for b in "abc"
            for i in range(7)
        ]
    )
    first = make_splits(frame, cfg).sort_values("image_id").reset_index(drop=True)
    second = (
        make_splits(frame.sample(frac=1, random_state=1), cfg)
        .sort_values("image_id")
        .reset_index(drop=True)
    )
    pd.testing.assert_frame_equal(first, second)
    assert set(first[first.split == "label"].image_id).isdisjoint(
        first[first.split == "test"].image_id
    )
    assert first.groupby(["temp_bin", "split"]).size().min() >= 2


def test_failed_artifact_is_resumable(tmp_path):
    def failure(folder):
        atomic_json(folder / "checkpoint.json", {"n": 1})
        raise RuntimeError("interrupted")

    with pytest.raises(RuntimeError):
        build(tmp_path, "test", {}, failure)

    def resume(folder):
        assert json.loads((folder / "checkpoint.json").read_text()) == {"n": 1}
        atomic_json(folder / "done.json", {"n": 2})

    path, _ = build(tmp_path, "test", {}, resume)
    verify(path)


def test_identities_are_canonical():
    assert digest({"a": 1, "b": 2}) == digest({"b": 2, "a": 1})
    assert task_seed(42, "ab", "c") != task_seed(42, "a", "bc")
