from __future__ import annotations

import numpy as np
import pandas as pd

from ..config import tier_map
from ..metrics.distribution import sliced_wasserstein
from ..provenance import atomic_json, task_seed


def make_splits(meta, cfg):
    """Hash-ranked stable IDs: deterministic, disjoint, nonempty halves even for sparse bins."""
    records = []
    for concept in sorted(cfg["experiment"]["concepts"]):
        for b in cfg["experiment"]["temporal_bins"]:
            ids = meta.loc[(meta.concept == concept) & (meta.temp_bin == b), "image_id"].tolist()
            ids.sort(key=lambda image_id: (task_seed(cfg["seed"], "split", image_id), image_id))
            if len(ids) < cfg["split"]["minimum_per_bin"]:
                continue
            cut = max(2, min(len(ids) - 2, int(len(ids) * cfg["split"]["label_fraction"])))
            records.extend(
                {
                    "image_id": image_id,
                    "concept": concept,
                    "temp_bin": b,
                    "split": "label" if i < cut else "test",
                }
                for i, image_id in enumerate(ids)
            )
    return pd.DataFrame(records, columns=["image_id", "concept", "temp_bin", "split"])


def fit_taxonomy(cfg, folder, embs, meta):
    from sklearn.cluster import KMeans

    splits = make_splits(meta, cfg)
    splits.to_csv(folder / "splits.csv", index=False)
    selected = meta.merge(
        splits[["image_id", "split"]], on="image_id", how="left", validate="one_to_one"
    )
    b0, _, b2 = cfg["experiment"]["temporal_bins"]
    records = []
    for concept in sorted(cfg["experiment"]["concepts"]):
        result = {"concept": concept, "tier": tier_map(cfg)[concept]}
        for split, name in [("label", "proxy_swd"), ("test", "vis_swd_test")]:
            indices = [
                selected.index[
                    (selected.concept == concept)
                    & (selected.temp_bin == b)
                    & (selected.split == split)
                ].to_numpy()
                for b in (b0, b2)
            ]
            result[name] = sliced_wasserstein(
                embs[indices[0]],
                embs[indices[1]],
                projections=cfg["experiment"]["n_proj_swd"],
                order=cfg["metrics"]["swd_order"],
                seed=cfg["seed"],
            )
        records.append(result)
    frame = pd.DataFrame(records)
    valid = frame.dropna(subset=["proxy_swd", "vis_swd_test"]).sort_values(
        ["proxy_swd", "concept"], kind="stable"
    )
    if len(valid) < 3:
        raise ValueError("At least three concepts with valid labeling and test splits are required")
    labels = {}
    for tier, group in zip(["stable", "slow", "fast"], np.array_split(valid.concept.to_numpy(), 3)):
        labels.update({c: tier for c in group})
    frame["dd_tier"] = frame.concept.map(labels)
    # Clustering is supplementary. Its labels never silently replace the primary taxonomy.
    values = valid[["proxy_swd"]].to_numpy()
    n_clusters = min(3, len(np.unique(values)))
    km = KMeans(n_clusters=n_clusters, random_state=cfg["seed"], n_init=50).fit(values)
    order = np.argsort(km.cluster_centers_.ravel())
    km_map = {int(k): ["stable", "slow", "fast"][i] for i, k in enumerate(order)}
    assignments = dict(zip(valid.concept, [km_map[int(k)] for k in km.labels_]))
    frame["km_tier"] = frame.concept.map(assignments)
    frame.to_csv(folder / "taxonomy.csv", index=False)
    atomic_json(folder / "taxonomy.json", labels)
    return frame
