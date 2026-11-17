from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..data.inventory import check_image
from ..models.embeddings import load_text, load_visual, save_array
from ..analysis.evaluate import query


def finish(fig, folder, name):
    fig.tight_layout()
    fig.savefig(folder / f"{name}.png", dpi=150, metadata={"Software": "temporal-drift-vlm"})
    plt.close(fig)


def plot_results(cfg, folder, paths):
    plt.rcParams.update(
        {"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False}
    )
    all_metrics = pd.read_csv(paths["metrics"] / "master_results.csv")
    metrics = all_metrics[all_metrics.split == "full"]
    comparison = metrics.drop_duplicates(["concept", "model"]).pivot(
        index="concept", columns="model", values="vis_swd"
    )
    comparison = comparison.sort_values("clip", ascending=False)
    ax = comparison.plot.bar(figsize=(max(12, len(comparison) * 0.35), 5))
    ax.set_ylabel("Visual SWD")
    finish(ax.figure, folder, "model_comparison_swd")

    text = metrics[metrics.model == "clip"]
    pivot = text.pivot(index="concept", columns="language", values="text_delta").reindex(
        comparison.index
    )
    fig, axes = plt.subplots(
        1, 2, figsize=(12, max(5, len(pivot) * 0.2)), gridspec_kw={"width_ratios": [1, 5]}
    )
    image = axes[0].imshow(comparison[["clip"]], aspect="auto", cmap="YlOrRd")
    fig.colorbar(image, ax=axes[0])
    image = axes[1].imshow(pivot, aspect="auto", cmap="YlOrRd")
    fig.colorbar(image, ax=axes[1])
    for ax in axes:
        ax.set_yticks(range(len(pivot)), labels=pivot.index, fontsize=7)
    axes[0].set_xticks([0], labels=["Visual SWD"])
    axes[1].set_xticks(range(len(pivot.columns)), labels=pivot.columns)
    axes[1].set_title("Text direction drift (M-CLIP)")
    finish(fig, folder, "drift_heatmap")

    for kind in ["trajectory", "normalize"]:
        if kind not in paths:
            continue
        trajectory = pd.read_csv(paths[kind] / "trajectory_results.csv")
        for model, frame in trajectory.groupby("model"):
            frame = frame.sort_values("delta_theta", ascending=False)
            fig, ax = plt.subplots(figsize=(max(12, len(frame) * 0.35), 5))
            x = np.arange(len(frame))
            ax.scatter(x, frame.theta_vis, label="Observed")
            ax.scatter(x, frame.null_median, marker="x", label="Concept-specific null median")
            ax.set_xticks(x, labels=frame.concept, rotation=90)
            ax.set_ylabel("Trajectory angle (degrees)")
            ax.legend()
            finish(fig, folder, f"trajectory_{kind}_{model}")
    taxonomy = pd.read_csv(paths["taxonomy"] / "taxonomy.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, column in zip(axes, ["tier", "dd_tier"]):
        taxonomy.groupby(column).vis_swd_test.mean().reindex(["stable", "slow", "fast"]).plot.bar(
            ax=ax
        )
        ax.set_title(column)
        ax.set_ylabel("Held-out visual SWD")
    finish(fig, folder, "h1_taxonomy_comparison")
    language = text.groupby("language").text_delta.agg(["mean", "sem"])
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(language.index, language["mean"], yerr=language["sem"])
    ax.set_ylabel("Text direction drift")
    finish(fig, folder, "h2_text_delta")
    if "statistics" in paths:
        regimes = pd.read_csv(paths["statistics"] / "regimes.csv")
        fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True, sharey=True)
        colors = {
            "drifting": "#e15759",
            "frozen": "#4e79a7",
            "noisy": "#f28e2b",
            "ambiguous": "#b07aa1",
        }
        for ax, (language, frame) in zip(axes.flat, regimes.groupby("language")):
            ax.scatter(frame.text_delta, frame.text_sigma2_mean, c=frame.regime.map(colors))
            ax.axvline(regimes.text_delta.median(), color="gray", linestyle="--")
            ax.axhline(regimes.text_sigma2_mean.median(), color="gray", linestyle="--")
            ax.set_title(language)
            ax.set_xlabel("Text drift")
            ax.set_ylabel("Paraphrase variance")
        finish(fig, folder, "h2_regimes")
    if "retrieval" in paths:
        retrieval = pd.read_csv(paths["retrieval"] / "retrieval_quality.csv")
        retrieval[retrieval.k == 10].groupby(["language", "model"]).AP.mean().unstack().plot.bar(
            figsize=(10, 4), ylabel="Corrected MAP@10"
        )
        finish(plt.gcf(), folder, "retrieval_map10")
    if "normalize" in paths:
        sensitivity = pd.read_csv(paths["normalize"] / "normalization_sensitivity.csv").set_index(
            "concept"
        )
        sensitivity[["vis_swd", "vis_swd_sn"]].plot.bar(
            figsize=(max(12, len(sensitivity) * 0.35), 5)
        )
        finish(plt.gcf(), folder, "color_normalization_sensitivity")
    if "style" in paths:
        style = pd.read_csv(paths["style"] / "style_metrics.csv")
        joint = (
            metrics[metrics.model == "clip"].drop_duplicates("concept").merge(style, on="concept")
        )
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        for ax, column in zip(axes, ["style_swd", "delta_sharpness"]):
            ax.scatter(joint[column], joint.vis_swd)
            ax.set_xlabel(column)
            ax.set_ylabel("Visual SWD")
        finish(fig, folder, "artifact_controls")


def projections(cfg, folder, visual):
    from sklearn.decomposition import PCA
    from umap import UMAP

    for model in cfg["experiment"]["models"]:
        values, meta = load_visual(visual, model)
        coords = UMAP(
            n_components=2,
            n_neighbors=min(30, len(values) - 1),
            min_dist=0.1,
            metric="cosine",
            random_state=cfg["seed"],
            n_jobs=1,
        ).fit_transform(values)
        save_array(folder / f"umap_{model}.npy", coords)
        fig, ax = plt.subplots(figsize=(8, 6))
        for b in cfg["experiment"]["temporal_bins"]:
            mask = (meta.temp_bin == b).to_numpy()
            ax.scatter(*coords[mask].T, s=3, alpha=0.4, label=b)
        ax.legend()
        finish(fig, folder, f"umap_{model}")
        pca = PCA(n_components=2, svd_solver="full").fit(values)
        save_array(folder / f"pca_components_{model}.npy", pca.components_)
        save_array(folder / f"pca_mean_{model}.npy", pca.mean_)
        fig, axes = plt.subplots(
            int(np.ceil(len(cfg["experiment"]["concepts"]) / 4)),
            4,
            figsize=(16, max(4, len(cfg["experiment"]["concepts"]))),
        )
        for ax in np.asarray(axes).flat:
            ax.set_visible(False)
        from ..metrics.distribution import centroid

        for ax, concept in zip(np.asarray(axes).flat, cfg["experiment"]["concepts"]):
            pools = [
                values[((meta.concept == concept) & (meta.temp_bin == b)).to_numpy()]
                for b in cfg["experiment"]["temporal_bins"]
            ]
            if any(len(p) < 2 for p in pools):
                continue
            ax.set_visible(True)
            points = pca.transform(np.stack([centroid(p) for p in pools]))
            ax.plot(*points.T, "o-")
            ax.set_title(concept)
        finish(fig, folder, f"centroid_pca_{model}")


def retrieval_grids(cfg, folder, visual, text_path):
    for item in cfg["grids"]:
        concept, lang, model = item
        values, meta = load_visual(visual, model)
        texts, prompts = load_text(text_path, model)
        fig, axes = plt.subplots(3, 5, figsize=(14, 8))
        selected = []
        for axes_row, b in zip(axes, cfg["experiment"]["temporal_bins"]):
            q, _ = query(texts, prompts, concept, lang, b)
            ids = meta.index[(meta.concept == concept) & (meta.temp_bin == b)].to_numpy()
            ordered = ids[np.argsort(-(values[ids] @ q), kind="stable")[:5]]
            for ax in axes_row:
                ax.axis("off")
            for ax, index in zip(axes_row, ordered):
                row = meta.iloc[index]
                ax.imshow(check_image(Path(cfg["data_root"]), row))
                selected.append({"image_id": row.image_id, "temp_bin": b})
            axes_row[0].set_title(b)
        fig.suptitle(f"{concept} | {lang} | {model}")
        name = f"grid_{concept}_{lang}_{model}"
        finish(fig, folder, name)
        pd.DataFrame(selected).to_csv(folder / f"{name}.csv", index=False)
