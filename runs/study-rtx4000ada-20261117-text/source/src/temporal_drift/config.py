"""Validated, relocatable experiment configuration; no notebook globals."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path


def load_config(path: str | Path) -> dict:
    path = Path(path).resolve()
    cfg = json.loads(path.read_text(encoding="utf-8"))
    for key in ("experiment", "prompts", "sources"):
        ref = (path.parent / cfg[key]).resolve()
        cfg[key] = json.loads(ref.read_text(encoding="utf-8"))
    cfg["_config_path"] = str(path)
    for key in ("data_root", "artifact_root", "run_root"):
        cfg[key] = str((path.parent / cfg[key]).resolve())
    validate_config(cfg)
    return cfg


def validate_config(cfg: dict) -> None:
    e = cfg["experiment"]
    concepts = e["concepts"]
    if len(concepts) != len(set(concepts)) or not concepts:
        raise ValueError("Concepts must be nonempty and unique")
    tier_concepts = [c for cs in e["concept_tiers"].values() for c in cs]
    if sorted(tier_concepts) != sorted(concepts):
        raise ValueError("Each concept must belong to exactly one a priori tier")
    if len(e["temporal_bins"]) != 3:
        raise ValueError("Trajectory analysis requires exactly three temporal bins")
    if len(set(e["temporal_bins"])) != 3:
        raise ValueError("Temporal bins must be unique")
    if "clip" not in e["models"] or set(e["models"]) - {"clip", "m_openclip", "siglip2"}:
        raise ValueError("Model set must include clip and contain only supported adapters")
    if 10 not in e["k_values"] or any(k < 1 for k in e["k_values"]):
        raise ValueError("Positive retrieval cutoffs including k=10 are required")
    for lang in e["languages"]:
        if set(concepts) - cfg["prompts"]["CONCEPT_NAMES"][lang].keys():
            raise ValueError(f"Missing concept translations for {lang}")
        if e["resource_level"][lang] <= 0:
            raise ValueError("Resource estimates must be positive")
        for b in e["temporal_bins"]:
            if lang not in cfg["prompts"]["PERIOD_LABEL"][b]:
                raise ValueError(f"Missing period translation: {lang}/{b}")
    for value in concepts + e["temporal_bins"] + list(e["models"]):
        if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
            raise ValueError(f"Unsafe identifier: {value}")
    if cfg["metrics"]["swd_order"] not in (1, 2):
        raise ValueError("SWD order must be 1 or 2")
    if e["n_proj_swd"] < 1 or e["n_permutations"] < 1:
        raise ValueError("Projection/permutation counts must be positive")
    if not 0 < cfg["split"]["label_fraction"] < 1:
        raise ValueError("label_fraction must be between zero and one")
    if cfg["split"]["minimum_per_bin"] < 4:
        raise ValueError("At least four images per bin are needed for disjoint splits")
    if cfg["batch_size"] < 1 or cfg["threads"] < 1:
        raise ValueError("Batch size and thread count must be positive")
    for key in ("clip", "mclip", "m_openclip", "xlm_roberta", "siglip2", "dataset"):
        if not re.fullmatch(r"[0-9a-f]{40}", cfg["sources"][key]["revision"]):
            raise ValueError(f"{key} must use an immutable 40-character revision")


def scientific_config(cfg: dict) -> dict:
    """Machine-specific locations do not alter scientific identity."""
    return {
        k: copy.deepcopy(v)
        for k, v in cfg.items()
        if not k.startswith("_") and k not in {"data_root", "artifact_root", "run_root"}
    }


def tier_map(cfg: dict) -> dict[str, str]:
    return {c: t for t, cs in cfg["experiment"]["concept_tiers"].items() for c in cs}
