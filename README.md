# Temporal Drift in Visual Embedding Spaces of Multilingual Vision-Language Models

**Authors:**
- **Md Zunayedul Islam** — Universidad Autónoma de Madrid | mdz.islam@estudiante.uam.es
- **Dr. Marcos Escudero-Viñolo** — Universidad Autónoma de Madrid | marcos.escudero@uam.es

## Abstract

Contrastive vision-language models encode a shared embedding space implicitly anchored to the temporal distribution of their training data. This work presents the first systematic study of *temporal drift* in visual embedding spaces: the phenomenon by which concepts with changing visual appearance produce systematically different image distributions across historical periods.

Using **~49,304 timestamped photographs** from YFCC15M (2004–2014), we probe **47 visual concepts** across three semantic tiers with temporally-anchored prompts in **six typologically diverse languages**, comparing three architectures: CLIP, M-OpenCLIP, and SigLIP-2. Relative to the pilot study (V2, 18 concepts, ~19K images), this expanded experiment introduces a data-driven concept taxonomy derived from a held-out SWD proxy, two independent style-control methods confirming that all measured drift is predominantly semantic, a joint language-regime classification, and cross-model reliability analysis (ICC = 0.791). All three hypotheses are supported across both a priori and data-driven taxonomies.

## Hypotheses

| ID | Hypothesis |
|---|---|
| **H1** | Semantic tier is a significant predictor of visual distributional shift, directly or in interaction with linguistic resources |
| **H2** | Temporal text-direction drift is jointly predicted by language training-data volume and morphological typology |
| **H3** | Consecutive centroid displacements are directionally more consistent than a permutation-null baseline, indicating structured evolution |

## Dataset

- **Source:** YFCC15M (Flickr, CC-licensed)
- **Images:** ~49,304 photographs
- **Temporal bins:** `pre2008` · `2008_2011` · `2012_2014`
- **Target per (concept, bin):** 400 images
- **Valid concepts for analysis:** 47 

### Concepts (47 valid / 48 attempted, 3 a priori tiers)

| A Priori Tier | Concepts |
|---|---|
| **Stable** (nature, n=16) | mountain, river, ocean, forest, beach, moon, cloud, waterfall, desert, glacier, sunset, field, bridge, park, church, parade |
| **Slow** (institutions, n=20) | hospital, office, classroom, restaurant, library, surgery, airport, factory, stadium, railway, courtroom, supermarket, rally, concert, marathon, debate, ceremony, wedding, headphones, satellite |
| **Fast** (technology, n=12) | phone, protest, television, computer, camera, car, tablet, smartphone, laptop, drone, smartwatch†, robot |

† *smartwatch* is excluded from all analyses: it appears only in 2012–2014 (63 images), with no presence in the earlier two bins, reflecting genuine technological emergence rather than data sparsity.

### Data-Driven Taxonomy (tertile split on proxy SWD, n=47 valid concepts)

The a priori labels are validated against an independently derived data-driven taxonomy. The primary data-driven taxonomy uses a **tertile split** of per-concept SWD measured on a held-out labeling split (rows 0:200 per concept); k-means (k=3) is included as a robustness check. Spearman ρ between labeling-split SWD and test-split SWD is 0.894 (p<0.0001), confirming reliable drift measurement.

| Data-Driven Tier | Concepts (n) |
|---|---|
| **Stable** (n=15) | glacier, beach, waterfall, bridge, railway, moon, church, river, phone, desert, park, cloud, camera, airport, office |
| **Slow** (n=15) | restaurant, satellite, laptop, supermarket, factory, ocean, sunset, headphones, marathon, forest, parade, hospital, computer, car, smartphone |
| **Fast** (n=17) | tablet, protest, library, debate, stadium, courtroom, drone, wedding, classroom, television, robot, concert, mountain, ceremony, field, rally, surgery |

Notable tier reassignments (a priori → data-driven): *surgery* slow→fast (laparoscopic proliferation, robotic surgery), *field* stable→fast (agricultural photography shift), *mountain* stable→fast, *phone* fast→stable (canonical archetype lock), *camera* fast→stable.

### Languages (6)

| Language | Code | Resource level | Regime (majority, n=47) |
|---|---|---|---|
| English | `en` | High | noisy (25) + ambiguous (22) |
| Russian | `ru` | High | drifting (46) |
| Japanese | `ja` | High | drifting (42) |
| Arabic | `ar` | Medium | ambiguous (19) + noisy (18) + frozen (10) |
| Bengali | `bn` | Low | noisy (41) |
| Swahili | `sw` | Low | frozen (43) |

Regimes are defined by joint (Δ, σ²) classification of text direction drift per language × concept pair. JA and RU exhibit near-universal drifting, SW near-universal frozen (low drift and low variance), BN near-universal noisy (high variance, low drift), reflecting training-data volume effects.

## Models

| Model | Architecture | Embedding dim |
|---|---|---|
| [CLIP ViT-B/32](https://huggingface.co/openai/clip-vit-base-patch32) | ViT-B/32 | 512 |
| [M-OpenCLIP XLM-R ViT-B/32](https://huggingface.co/laion/CLIP-ViT-B-32-xlm-roberta-base-laion5B-s13B-b90k) | ViT-B/32 + XLM-RoBERTa | 512 |
| [SigLIP-2 base patch16-256](https://huggingface.co/google/siglip2-base-patch16-256) | ViT-B/16 | 768 |

## Metrics

| Metric | Symbol | Description |
|---|---|---|
| Sliced Wasserstein Distance | SWD | Full distributional divergence between embedding clouds (200 random projections) |
| Centroid Displacement | Δ | Cosine distance between L2-normalised mean embeddings |
| Text Direction Drift | δ | Cosine distance between temporally-anchored text embeddings |
| Trajectory Angle | θ_vis | Angle between consecutive centroid displacement vectors |
| Retrieved-image SWD | ret_swd_k10 | SWD of images retrieved by temporally-anchored queries (k=10, 50); unifies H1 and H2 in the LME |
| Mean Average Precision | MAP@k | Retrieval quality with neutral prompts at cutoffs k=10, 50 |
| Gram Style SWD | style_swd | SWD of VGG-16 Gram matrix features; measures photographic style shift |
| Style-Normalized SWD | vis_swd_sn | SWD after Reinhard LAB colour-transfer normalization to a global canonical style |
| ICC(A,1) | ICC | Intraclass correlation of per-concept SWD across the three model architectures |
| Semantic retention | pct_retained | Fraction of vis_swd surviving style normalization (vis_swd_sn / vis_swd × 100) |

## Key Results

### H1 — Concept-Tier Drift (SUPPORTED)

The unified LME (`ret_swd_k10 ~ tier × log_resource + (1|concept)`) shows:
- Fast tier main effect: p = 0.009 (**)
- Fast × log_resource interaction: p = 0.0004 (***)
- Data-driven taxonomy, test split: fast vs stable t = 4.81, d = 1.24 (large effect), p < 0.0001

H1 survives style control (style_swd covariate p = 0.127, n.s.), confirming the measured drift reflects genuine semantic change rather than photographic style shifts.

### H2 — Cross-Lingual Asymmetry (SUPPORTED)

- Spearman ρ(text_delta, ret_swd_k10) = 0.645, p < 0.0001 (n = 282)
- LME: log_resource coefficient = 0.0039, p < 0.0001
- Mean text_delta: JA = 0.056 (highest), SW = 0.015 (lowest)

Semantic fossilization: for 7 of 11 fast-drift concepts, EN queries retrieve *less* temporally diverse imagery than BN queries (EN/BN ret_swd ratio < 1), indicating that high-resource languages' text representations are anchored to historical visual archetypes.

### H3 — Trajectory Smoothness (SUPPORTED)

- Wilcoxon signed-rank W = 27.0, p < 0.0001 (one-sided, observed < null)
- Fast-drift concepts: mean Δθ = 27.8° below permutation null
- H3 survives style normalization (SN-CLIP: W = 46.0, p < 0.0001)

Trajectory anomalies: *protest* (Δθ = 0.46°, near-random — event-contingent, not aesthetic); *park* (θ = 131.2°, above null — atypical scattering); *surgery* highest SWD = 0.026 despite slow a priori classification.

### Cross-Model Reliability

ICC(A,1) = 0.791, 95% CI [0.21, 0.93] — **excellent** cross-model agreement. Drift ranks are largely model-independent, validating generalizability beyond individual architectures.

### Style Decomposition

All 47 concepts retain ≥ 85% of SWD after Reinhard LAB style normalization (range: 85.5% camera to 100% field). No concept loses ≥ 50% to style. Rank correlation of original vs. SN SWD: ρ = 0.987.

### Retrieval Quality (MAP@10)

| Model | EN | RU | JA | AR | BN | SW | Overall |
|---|---|---|---|---|---|---|---|
| CLIP | 0.801 | 0.736 | 0.730 | 0.545 | 0.128 | 0.175 | 0.519 |
| M-OpenCLIP | 0.823 | 0.795 | 0.769 | 0.725 | 0.338 | 0.173 | 0.604 |
| SigLIP-2 | 0.821 | 0.699 | 0.599 | 0.584 | 0.488 | 0.234 | 0.571 |

CLIP BN MAP@10 = 0.128 vs. SigLIP-2 BN = 0.488 — the starkest multilingual gap, demonstrating that model architecture fundamentally determines low-resource language alignment.

## Repository Structure

```
.
├── t-Drift-VLM_48c.ipynb              # Main research notebook (all experiments with 48 concepts)
├── t-Drift-VLM_18c.ipynb              # Secondary research notebook (initial experiments with 18 concepts)
├── metadata/
│   └── yfcc_filtered_metadata.csv     # Filtered YFCC15M metadata (54,960 rows)
├── images/
│   └── {concept}/{temporal_bin}/      # Downloaded Flickr images (~49K files)
├── embeddings/                        # L2-normalised visual + text embeddings (per model)
│   ├── clip_vitb32_embeddings.npy
│   ├── clip_vitb32_sn_embeddings.npy  # Style-normalised CLIP embeddings
│   ├── m_openclip_vitb32_embeddings.npy
│   ├── siglip2_ml_embeddings.npy
│   ├── mclip_text_embeddings.npy
│   ├── m_openclip_text_embeddings.npy
│   └── siglip2_ml_text_embeddings.npy
└── results/                           # All output figures and CSVs

```

## Results Files

All outputs are saved to `results/`. Key files:

| File | Description |
|---|---|
| `master_results.csv` | Full per-(model, concept, language) metrics (846 rows: 3 × 47 × 6) |
| `icc_results.csv` | Intraclass correlation across architectures |
| `trajectory_results.csv` | Centroid trajectory angles (original + SN) |
| `retrieval_quality.csv` | MAP@k retrieval scores (all models × languages × k) |
| `retrieval_summary.csv` | Aggregated MAP@10 cross-model summary |
| `style_gram_swd.json` | VGG-16 Gram matrix style SWD per concept |
| `lab_global_stats.json` | Global LAB mean/std for Reinhard normalization |
| `dd_proxy_swd.json` | Proxy SWD per concept (labeling split) |
| `dd_test_indices.json` | Test-split indices for each concept × bin |
| `drift_heatmap.png` | Visual SWD × text drift heatmap across concepts and languages |
| `umap_{model}.png` | UMAP projections of visual embedding spaces |
| `visual_centroid_trajectory_{model}.png` | PCA centroid trajectories (3 models) |
| `model_comparison_swd.png` | Per-concept SWD across CLIP / M-OpenCLIP / SigLIP-2 |
| `icc_model_comparison.png` | Per-concept variance decomposition across models |
| `h2_text_delta_bar.png` | Text direction drift by language and tier |
| `h2_regime_scatter.png` | Joint (Δ, σ²) regime classification scatter |
| `h3_sn_trajectory_angles.png` | Style-normalized H3 trajectory angle comparison |

## Reproducing the Experiments

### 1. Install dependencies

```bash
pip install aiohttp nest_asyncio datasets regex python-dotenv \
            tqdm pandas matplotlib seaborn pingouin \
            transformers sentencepiece ftfy scikit-learn scikit-image \
            umap-learn sentence-transformers timm POT \
            statsmodels opencv-python-headless open-clip-torch
```

### 2. Run the notebook

Open `t-Drift-VLM_{18/48}c.ipynb` and execute cells sequentially. The notebook is fully self-contained and covers:

1. **Data Detection** — per-concept, per-bin image inventory; identification of under-quota concepts
2. **YFCC15M Streaming** — targeted metadata streaming scoped to under-quota bins only
3. **Image Download** — threaded download via `requests` (ThreadPoolExecutor, 40 workers)
4. **Embedding Extraction** — incremental, concept×bin-level extraction for all three models; skips already-embedded pairs; deduplicates on re-run
5. **Text Embeddings** — temporally-anchored and neutral prompts across all models and 6 languages
6. **Core Drift Metrics** — SWD, centroid displacement, text drift, trajectory angle
7. **Model Comparison** — per-concept SWD across architectures, ICC cross-model reliability
8. **Trajectory Analysis** — visual centroid trajectories with 1,000-iteration permutation null
9. **Proxy SWD + Data-Driven Taxonomy** — labeling/test split; tertile (primary) and k-means (robustness) taxonomies; staleness-checked cache
10. **H1 (Unified LME)** — `ret_swd_k10 ~ tier × log_resource + (1|concept)` on both a priori and data-driven taxonomies
11. **H2 (Cross-Lingual Asymmetry)** — Spearman + LME on text direction drift; regime classification
12. **H3 (Trajectory Smoothness)** — Wilcoxon signed-rank test; fast-tier subset analysis
13. **Artifact Controls** — sharpness (Laplacian variance), style (VGG-16 Gram SWD), style-controlled LME
14. **Style Normalization** — Reinhard LAB transfer to global canonical style; style-normalized CLIP embeddings; SN-SWD decomposition; SN trajectory H3
15. **Retrieval Evaluation** — MAP@k cross-lingual retrieval; semantic fossilization analysis (EN/BN SWD ratio)
16. **Visualizations** — UMAP, drift heatmap, centroid trajectories, retrieval bar chart, regime scatter

### 3. Reproducibility

Global seed is fixed to `42` across NumPy, PyTorch, Python `random`, and `PYTHONHASHSEED`. All expensive computations (visual embeddings, text embeddings, proxy SWD, style SWD, sharpness, LAB stats) are cached to disk; re-runs load from cache. Proxy SWD cache includes an embedding-matrix staleness check (max index vs. current matrix size).

**GPU required for reasonable runtime** — Authors used **NVIDIA A40** GPU (48GB VRAM) for 48 concepts and **NVIDIA T4** GPU (16GB VIRAM) for 18 concepts. If the `embeddings`, `images`, and `metadata` are already available on the disk, all notebooks will feasibly run on the CPU. Note that, the notebooks are capable of detecting CUDA automatically and falling back to CPU.

## Statistical Tests

| Hypothesis | Primary Test | Secondary |
|---|---|---|
| H1 | Unified LME: `ret_swd_k10 ~ C(tier) × log_resource + (1\|concept)` | Paired permutation test + Cohen's d; Kruskal-Wallis + Mann-Whitney on vis_swd_sn |
| H2 | Spearman ρ(text_delta, ret_swd_k10) | LME: `text_delta ~ log_resource + (1\|concept)` |
| H3 | Wilcoxon signed-rank, one-sided (observed < permutation null) | 1,000-iteration permutation null; repeated on style-normalized embeddings |

Significance level: α = 0.05. All hypotheses are pre-specified. The data-driven taxonomy is derived on a labeling split (rows 0:200 per concept) and evaluated on a held-out test split (rows 200:400), preventing data leakage into taxonomy construction.

## Pilot Study

| Dimension | 18c | 48c |
|---|---|---|
| Concepts | 18 (6+6+6) | 47 valid / 48 attempted (16+20+11+1 excluded) |
| Images | ~19,334 | ~49,304 |
| Taxonomy | A priori only | A priori + data-driven (tertile + k-means, held-out split) |
| Tier × language unification | Separate H1/H2 tests | Unified LME on `ret_swd_k10` |
| Style controls | None | VGG-16 Gram SWD + Reinhard LAB normalization (both independent) |
| Style-normalized embeddings | None | SN-CLIP; SN trajectory H3; SN style decomposition per concept |
| Cross-model reliability | Not measured | ICC(A,1) = 0.791 (excellent) |
| Sharpness artifact check | None | Laplacian variance correlation (ρ = 0.043, p = 0.776 — no artifact) |
| Regime classification | None | Joint (Δ, σ²) per language: drifting / frozen / noisy / ambiguous |
| Semantic fossilization | Not characterized | EN/BN retrieval SWD ratio < 1 for 7/11 fast concepts |
| Emergent-concept evidence | None | Smartwatch: genuine pre-2012 absence confirmed (0 images across 14.5M rows) |
| Anomaly spotlight | None | Protest (near-random θ), surgery (slow→fast reclassification), park (above-null θ) |
| Cache robustness | Basic | Embedding-matrix staleness check; SN deduplication on re-embed |
| H1 effect size (data-driven) | — | Cohen's d = 1.24 (large), p < 0.0001 |

## Citation

If you use this work, please cite:

```bibtex
@misc{islam2026temporaldrift,
  title   = {Temporal Drift in Visual Embedding Spaces of Multilingual Vision-Language Models},
  author  = {Islam, Md Zunayedul and Escudero-Vi{\~n}olo, Marcos},
  year    = {2026},
  institution = {Universidad Autónoma de Madrid},
}
```

## License

Images are sourced from YFCC15M under their original CC licenses (Attribution / Attribution-ShareAlike / Attribution-NonCommercial-NoDerivs). Code in this repository is released under the Apache License 2.0.
