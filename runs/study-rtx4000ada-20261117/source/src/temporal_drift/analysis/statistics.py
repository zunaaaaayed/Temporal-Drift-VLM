"""Explicit analysis populations, independent group tests, and machine-readable fits."""

from __future__ import annotations

import warnings
import json

import numpy as np
import pandas as pd
from scipy.stats import kruskal, mannwhitneyu, spearmanr, wilcoxon

from ..provenance import atomic_json, task_seed


def clean(value):
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        return float(value) if np.isfinite(value) else None
    return value


def independent_contrast(a, b, *, seed, permutations):
    """One-sided independent-label permutation; unequal groups retain every concept."""
    a, b = np.asarray(a), np.asarray(b)
    observed = float(a.mean() - b.mean())
    joined = np.r_[a, b]
    rng = np.random.default_rng(seed)
    count = 0
    for _ in range(permutations):
        shuffled = rng.permutation(joined)
        count += shuffled[: len(a)].mean() - shuffled[len(a) :].mean() >= observed
    pooled = np.sqrt(
        ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    )
    return {
        "difference": observed,
        "permutation_p": (count + 1) / (permutations + 1),
        "cohen_d_independent": float(observed / pooled) if pooled else None,
        "mann_whitney_p": float(mannwhitneyu(a, b, alternative="greater").pvalue),
        "n_a": len(a),
        "n_b": len(b),
    }


def mixed_model(data, formula):
    import statsmodels.formula.api as smf

    try:
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always")
            fit = smf.mixedlm(formula, data, groups=data.concept).fit(reml=True)
        return {
            "formula": formula,
            "n": len(data),
            "concepts": data.concept.nunique(),
            "converged": bool(fit.converged),
            "coefficients": fit.fe_params.to_dict(),
            "pvalues": fit.pvalues.to_dict(),
            "confidence_intervals": fit.conf_int().to_dict(),
            "random_intercept_variance": float(fit.cov_re.iloc[0, 0]),
            "warnings": [str(w.message) for w in captured],
            "summary": str(fit.summary()),
        }
    except Exception as exc:
        return {"formula": formula, "n": len(data), "error": str(exc)}


def holm(pvalues):
    """Holm family-wise adjustment; retain raw values beside adjusted ones."""
    names = sorted(pvalues, key=pvalues.get)
    result, previous = {}, 0.0
    for rank, name in enumerate(names):
        previous = max(previous, min(1.0, pvalues[name] * (len(names) - rank)))
        result[name] = previous
    return result


def analyze(
    cfg, folder, metrics_path, taxonomy_path, trajectory_path, style_path=None, sn_path=None
):
    all_data = pd.read_csv(metrics_path / "master_results.csv")
    taxonomy = pd.read_csv(taxonomy_path / "taxonomy.csv")
    tests = {}
    for model in cfg["experiment"]["models"]:
        # The primary H1 DV is recomputed exclusively from held-out images.
        data = all_data[(all_data.model == model) & (all_data.split == "test")].merge(
            taxonomy[["concept", "dd_tier"]], on="concept", validate="many_to_one"
        )
        for column in ["tier", "dd_tier"]:
            fit_data = data.dropna(subset=[column]).copy()
            fit_data["log_resource_centered"] = fit_data.log_resource - fit_data.log_resource.mean()
            formula = f"ret_swd_k10 ~ C({column}, Treatment('stable')) * log_resource_centered"
            tests[f"H1/{model}/{column}/lme"] = mixed_model(fit_data, formula)
            visual = fit_data.drop_duplicates("concept")
            groups = [
                visual.loc[visual[column] == t, "vis_swd"].to_numpy()
                for t in ["stable", "slow", "fast"]
            ]
            if all(len(g) >= 2 for g in groups):
                tests[f"H1/{model}/{column}/kruskal"] = dict(
                    zip(["statistic", "pvalue"], map(float, kruskal(*groups)))
                )
                contrasts = {}
                for target, other in [("fast_vs_stable", 0), ("fast_vs_slow", 1)]:
                    contrasts[target] = independent_contrast(
                        groups[2],
                        groups[other],
                        seed=task_seed(cfg["seed"], model, column, target),
                        permutations=cfg["statistical_permutations"],
                    )
                adjusted = holm({k: v["permutation_p"] for k, v in contrasts.items()})
                for k, v in contrasts.items():
                    v["holm_p"] = adjusted[k]
                tests[f"H1/{model}/{column}/contrasts"] = contrasts
        if style_path is not None:
            style = pd.read_csv(style_path / "style_metrics.csv")
            controlled = data.merge(style[["concept", "style_swd"]], on="concept")
            controlled = controlled.dropna(subset=["style_swd"])
            controlled["log_resource_centered"] = (
                controlled.log_resource - controlled.log_resource.mean()
            )
            tests[f"H1/{model}/style_control"] = mixed_model(
                controlled,
                "ret_swd_k10 ~ C(tier, Treatment('stable')) * log_resource_centered + style_swd",
            )

    # Delta uses M-CLIP only; do not count repeated visual models as independent evidence.
    text = all_data[(all_data.model == "clip") & (all_data.split == "full")].copy()
    rho, p = spearmanr(text.log_resource, text.text_delta)
    tests["H2/pooled_descriptive"] = {
        "rho": float(rho),
        "nominal_p": float(p),
        "n_pairs": len(text),
        "n_languages": text.language.nunique(),
    }
    languages = text.groupby("language")[["log_resource", "text_delta"]].mean()
    observed = float(spearmanr(languages.log_resource, languages.text_delta).statistic)
    # Enumerate language-level permutations for n<=8, respecting the true resource-level unit.
    import itertools

    if len(languages) <= 8:
        values = [
            float(spearmanr(languages.log_resource, perm).statistic)
            for perm in itertools.permutations(languages.text_delta)
        ]
        tests["H2/language_level"] = {
            "rho": observed,
            "n_languages": len(languages),
            "exact_one_sided_p": float(np.mean(np.asarray(values) >= observed - 1e-12)),
        }
    languages.to_csv(folder / "h2_language_summary.csv")
    text["text_sigma2_mean"] = (text.text_sigma2_pre + text.text_sigma2_post) / 2
    d, s = text.text_delta.median(), text.text_sigma2_mean.median()
    text["regime"] = np.select(
        [
            (text.text_delta >= d) & (text.text_sigma2_mean <= s),
            (text.text_delta < d) & (text.text_sigma2_mean <= s),
            (text.text_delta < d) & (text.text_sigma2_mean > s),
        ],
        ["drifting", "frozen", "noisy"],
        default="ambiguous",
    )
    text.to_csv(folder / "regimes.csv", index=False)
    text.groupby(["language", "regime"]).size().unstack(fill_value=0).to_csv(
        folder / "regime_counts.csv"
    )
    for name, path in [("original", trajectory_path), ("color_normalized", sn_path)]:
        if path is None:
            continue
        trajectories = pd.read_csv(path / "trajectory_results.csv")
        for model, frame in trajectories.groupby("model"):
            differences = (frame.theta_vis - frame.null_median).dropna()
            if len(differences):
                w, p = (
                    wilcoxon(differences, alternative="less") if differences.ne(0).any() else (0, 1)
                )
                tests[f"H3/{model}/{name}"] = {
                    "W": float(w),
                    "pvalue": float(p),
                    "n_concepts": len(differences),
                    "below_null": int((differences < 0).sum()),
                }
    if style_path is not None:
        style = pd.read_csv(style_path / "style_metrics.csv")
        visual = all_data[(all_data.model == "clip") & (all_data.split == "full")].drop_duplicates(
            "concept"
        )
        merged = visual.merge(style, on="concept")
        for column in ["style_swd", "delta_sharpness"]:
            pairs = merged.dropna(subset=[column, "vis_swd"])
            if len(pairs) >= 3:
                rho, p = spearmanr(pairs.vis_swd, pairs[column])
                tests[f"artifact/{column}"] = {
                    "rho": float(rho),
                    "pvalue": float(p),
                    "n": len(pairs),
                }
    if sn_path is not None:
        normalized = pd.read_csv(sn_path / "normalization_heldout.csv").merge(
            taxonomy, on="concept"
        )
        for column in ["tier", "dd_tier"]:
            groups = [
                normalized.loc[normalized[column] == t, "vis_swd_sn_test"].dropna().to_numpy()
                for t in ["stable", "slow", "fast"]
            ]
            if all(len(g) >= 2 for g in groups):
                statistic, pvalue = kruskal(*groups)
                tests[f"H1/clip/{column}/normalized_heldout"] = {
                    "kruskal_statistic": float(statistic),
                    "pvalue": float(pvalue),
                    "n_concepts": sum(map(len, groups)),
                }
    # Absolute agreement and consistency ICC are reported separately.
    ratings = all_data[all_data.split == "full"].drop_duplicates(["concept", "model"])
    if cfg.get("compute_icc", True):
        try:
            import pingouin as pg

            pg.intraclass_corr(
                data=ratings, targets="concept", raters="model", ratings="vis_swd"
            ).to_csv(folder / "icc_results.csv", index=False)
        except ImportError:
            tests["ICC"] = {"status": "not_computed", "reason": "Install the viz extra"}
    atomic_json(folder / "tests.json", clean(tests))
    lines = [
        "# Statistical results",
        "",
        "Generated from this run's artifacts; no copied paper values.",
        "",
        "Primary H1 comparisons use held-out image pools. H2 resource inference uses languages",
        "as its sampling unit. Nominal pooled H2 p-values are descriptive only.",
        "",
    ]
    for key, result in tests.items():
        lines.extend([f"## {key}", "", "```json", json.dumps(clean(result), indent=2), "```", ""])
    (folder / "REPORT.md").write_text("\n".join(lines))
