from __future__ import annotations

import numpy as np
import pandas as pd

from ..config import tier_map
from ..metrics.distribution import centroid, cosine_distance, normalize, sliced_wasserstein, top_k
from ..metrics.retrieval import average_precision_at_k, expected_random_ap, legacy_ap_at_k
from ..metrics.trajectory import angle, trajectory
from ..models.embeddings import load_text, load_visual, save_array
from ..provenance import task_seed


def swd(cfg, a, b):
    return sliced_wasserstein(
        a,
        b,
        projections=cfg["experiment"]["n_proj_swd"],
        order=cfg["metrics"]["swd_order"],
        seed=cfg["seed"],
    )


def query(text, prompts, concept, lang, b):
    mask = (prompts.concept == concept) & (prompts.language == lang) & (prompts.temp_bin == b)
    paraphrases = text[mask.to_numpy()]
    if len(paraphrases) != 3:
        raise ValueError(f"Expected three paraphrases for {concept}/{lang}/{b}")
    return normalize(paraphrases.mean(axis=0)), float(np.var(paraphrases, axis=0).mean())


def compute_metrics(cfg, folder, visual, text_path, taxonomy_path):
    e = cfg["experiment"]
    b0, _, b2 = e["temporal_bins"]
    splits = pd.read_csv(taxonomy_path / "splits.csv")
    records = []
    mclip, prompts = load_text(text_path, "clip")
    for model in e["models"]:
        values, meta = load_visual(visual, model)
        own_text, own_prompts = load_text(text_path, model)
        split_by_id = dict(zip(splits.image_id, splits.split))
        test_mask = meta.image_id.map(split_by_id).eq("test").to_numpy()
        for concept in sorted(e["concepts"]):
            for split in ["full", "test"]:
                pools = []
                for b in (b0, b2):
                    mask = ((meta.concept == concept) & (meta.temp_bin == b)).to_numpy()
                    if split == "test":
                        mask &= test_mask
                    pools.append(values[mask])
                if any(len(p) < 2 for p in pools):
                    continue
                pre, post = pools
                visual_swd = swd(cfg, pre, post)
                for lang in e["languages"]:
                    q0, s0 = query(mclip, prompts, concept, lang, b0)
                    q2, s2 = query(mclip, prompts, concept, lang, b2)
                    own0, _ = query(own_text, own_prompts, concept, lang, b0)
                    own2, _ = query(own_text, own_prompts, concept, lang, b2)
                    record = {
                        "model": model,
                        "concept": concept,
                        "tier": tier_map(cfg)[concept],
                        "language": lang,
                        "split": split,
                        "log_resource": float(np.log(e["resource_level"][lang])),
                        "vis_swd": visual_swd,
                        "vis_centroid_delta": cosine_distance(centroid(pre), centroid(post)),
                        "vis_disp_pre": float(np.var(pre, axis=0).mean()),
                        "vis_disp_post": float(np.var(post, axis=0).mean()),
                        "text_delta": cosine_distance(q0, q2),
                        "text_sigma2_pre": s0,
                        "text_sigma2_post": s2,
                        "theta_text": angle(
                            [query(mclip, prompts, concept, lang, b)[0] for b in e["temporal_bins"]]
                        ),
                        "n_pre": len(pre),
                        "n_post": len(post),
                    }
                    for k in e["k_values"]:
                        record[f"ret_swd_k{k}"] = swd(
                            cfg, top_k(pre, own0, k), top_k(post, own2, k)
                        )
                    records.append(record)
    frame = pd.DataFrame(records)
    if frame.empty:
        raise ValueError("No valid early/late comparisons")
    frame.to_csv(folder / "master_results.csv", index=False)
    frame[frame.split == "test"].to_csv(folder / "heldout_results.csv", index=False)


def compute_trajectories(cfg, folder, visual, *, suffix=""):
    records = []
    for model in cfg["experiment"]["models"]:
        values, meta = load_visual(visual, model)
        for concept in sorted(cfg["experiment"]["concepts"]):
            pools = [
                values[((meta.concept == concept) & (meta.temp_bin == b)).to_numpy()]
                for b in cfg["experiment"]["temporal_bins"]
            ]
            if any(len(p) < 2 for p in pools):
                continue
            result = trajectory(
                pools,
                permutations=cfg["experiment"]["n_permutations"],
                seed=task_seed(cfg["seed"], "trajectory", model, concept, suffix),
            )
            null = result.pop("null_angles")
            save_array(folder / f"null-{model}-{concept}.npy", null)
            records.append(
                {"model": model, "concept": concept, "tier": tier_map(cfg)[concept], **result}
            )
    pd.DataFrame(records).to_csv(folder / "trajectory_results.csv", index=False)


def evaluate_retrieval(cfg, folder, visual, text_path):
    records = []
    for model in cfg["experiment"]["models"]:
        values, meta = load_visual(visual, model)
        texts, prompts = load_text(text_path, model)
        for lang in cfg["experiment"]["languages"]:
            for concept in sorted(meta.concept.unique()):
                q, _ = query(texts, prompts, concept, lang, "neutral")
                ranking = np.argsort(-(values @ q), kind="stable")
                relevance = meta.concept.to_numpy()[ranking] == concept
                for k in cfg["experiment"]["k_values"]:
                    records.append(
                        {
                            "model": model,
                            "concept": concept,
                            "language": lang,
                            "k": k,
                            "precision": float(relevance[:k].mean()),
                            "AP": average_precision_at_k(relevance, k),
                            "legacy_AP": legacy_ap_at_k(relevance, k),
                            "random_precision": float(relevance.mean()),
                            "random_AP": expected_random_ap(len(values), int(relevance.sum()), k),
                            "n_gallery": len(values),
                            "n_relevant": int(relevance.sum()),
                        }
                    )
    frame = pd.DataFrame(records)
    frame.to_csv(folder / "retrieval_quality.csv", index=False)
    frame.groupby(["model", "language", "k"])[
        ["precision", "AP", "legacy_AP", "random_precision", "random_AP"]
    ].mean().to_csv(folder / "retrieval_summary.csv")
