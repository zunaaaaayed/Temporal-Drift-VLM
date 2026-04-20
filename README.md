# Temporal Drift in Visual Embedding Spaces of Multilingual Vision-Language Models

**Authors:**
- **Md Zunayedul Islam** — Universidad Autónoma de Madrid | mdz.islam@estudiante.uam.es
- **Dr. Marcos Escudero-Viñolo** — Universidad Autónoma de Madrid | marcos.escudero@uam.es

## Abstract

Contrastive vision-language models encode a shared embedding space implicitly anchored to the temporal distribution of their training data. This work presents the first systematic study of *temporal drift* in visual embedding spaces: the phenomenon by which concepts with changing visual appearance produce systematically different image distributions across historical periods.

Using **19,334 timestamped photographs** from YFCC15M (2004–2014), we probe **18 visual concepts** across three semantic tiers with temporally-anchored prompts in **six typologically diverse languages**, comparing three architectures: CLIP, M-OpenCLIP, and SigLIP-2.

## Hypotheses

| ID | Hypothesis |
|---|---|
| **H1** | Semantic tier is a significant predictor of visual distributional shift, directly or in interaction with linguistic resources |
| **H2** | Temporal text-direction drift is jointly predicted by language training-data volume and morphological typology |
| **H3** | Consecutive centroid displacements are directionally more consistent than a permutation-null baseline, indicating structured evolution |

## Dataset

- **Source:** YFCC15M (Flickr, CC-licensed)
- **Images:** ~19,334 photographs
- **Temporal bins:** `pre2008` · `2008_2011` · `2012_2014`
- **Target per (concept, bin):** 400 images

### Concepts (18 total, 3 tiers)

| Tier | Concepts |
|---|---|
| **Stable** (nature) | mountain, river, ocean, forest, beach, moon |
| **Slow** (institutions) | hospital, office, classroom, restaurant, library, surgery |
| **Fast** (technology) | phone, protest, television, computer, camera, car |

### Languages (6)

| Language | Code | Resource level |
|---|---|---|
| English | `en` | High |
| Russian | `ru` | High |
| Japanese | `ja` | High |
| Arabic | `ar` | Medium |
| Bengali | `bn` | Low |
| Swahili | `sw` | Low |

## Models

| Model | Architecture | Embedding dim |
|---|---|---|
| [CLIP ViT-B/32](https://huggingface.co/openai/clip-vit-base-patch32) | ViT-B/32 | 512 |
| [M-OpenCLIP XLM-R ViT-B/32](https://huggingface.co/laion/CLIP-ViT-B-32-xlm-roberta-base-laion5B-s13B-b90k) | ViT-B/32 + XLM-RoBERTa | 512 |
| [SigLIP-2 base patch16-256](https://huggingface.co/google/siglip2-base-patch16-256) | ViT-B/16 | 768 |

## Metrics

| Metric | Symbol | Description |
|---|---|---|
| Sliced Wasserstein Distance | SWD | Full distributional divergence between embedding clouds |
| Centroid Displacement | Δ | Cosine distance between L2-normalised mean embeddings |
| Text Direction Drift | δ | Cosine distance between temporally-anchored text embeddings |
| Trajectory Angle | θ_vis | Angle between consecutive centroid displacement vectors |
| Mean Average Precision | MAP@k | Retrieval quality with neutral prompts at cutoffs k=10,50 |

## Repository Structure

```
.
├── [V2]_Temporal_Drift_VLMs.ipynb   # Main research notebook (all experiments)
├── metadata/
│   └── yfcc_filtered_metadata.csv    # Filtered YFCC15M metadata
├── images/
│   └── {concept}/{temporal_bin}/     # Downloaded Flickr images
├── embeddings/                       # L2-normalised visual embeddings (per model)
├── results/                          # All output figures and CSVs
└── graphify-out/                     # Knowledge graph of codebase
```

## Results

All outputs are saved to `results/`. Key outputs include:

- `master_results.csv` — full per-(model, concept, language, bin) metrics
- `icc_results.csv` — intraclass correlation across architectures
- `trajectory_results.csv` — centroid trajectory angles
- `retrieval_quality.csv` — MAP@k retrieval scores
- `drift_heatmap.png` — visual SWD × text drift heatmap
- `umap_{model}.png` — UMAP projections of visual embedding spaces
- `visual_centroid_trajectory_{model}.png` — PCA centroid trajectories
- `h1_taxonomy_comparison.png`, `h2_text_delta_bar.png`, `h3_sn_trajectory_angles.png` — hypothesis figures

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

Open `[V2]_Temporal_Drift_VLMs.ipynb` and execute cells sequentially. The notebook is self-contained and covers:

1. **Data Pipeline** — YFCC15M streaming, image download, embedding extraction
2. **Text Embeddings** — temporally-anchored prompts across all models and languages
3. **Core Drift Metrics** — SWD, centroid displacement, text drift, trajectory angle
4. **Trajectory Analysis** — visual centroid trajectories across bins
5. **Data-Driven Taxonomy** — tertile split and k-means clustering on held-out split
6. **Statistical Tests** — H1/H2/H3 with LME, Spearman, and Wilcoxon tests
7. **Artifact Controls** — sharpness (Laplacian), style (VGG-16 Gram), Reinhard LAB normalisation
8. **Retrieval Evaluation** — MAP@k cross-lingual retrieval
9. **Visualizations** — UMAP, heatmaps, centroid trajectories, retrieval grids

### 3. Reproducibility

Global seed is fixed to `42` across NumPy, PyTorch, Python `random`, and `PYTHONHASHSEED`. All expensive computations (embeddings, SWD proxies) are cached to disk.

**GPU recommended** — the notebook detects CUDA automatically and falls back to CPU.

## Statistical Tests

| Hypothesis | Primary Test | Secondary |
|---|---|---|
| H1 | LME: tier × log-resource | Paired permutation + Cohen's d |
| H2 | Spearman rank correlation | LME: δ ~ log(resource) |
| H3 | Wilcoxon signed-rank (one-sided) | 1,000-iteration permutation null |

Significance level: α = 0.05. All hypotheses are pre-specified before data analysis.

## Citation

If you use this work, please cite:

```bibtex
@misc{islam2026temporaldrift,
  title   = {Temporal Drift in Visual Embedding Spaces of Multilingual Vision-Language Models},
  author  = {Islam, Md Zunayedul and Escudero-Viñolo, Marcos},
  year    = {2026},
  institution = {Universidad Aut{\'o}noma de Madrid},
}
```

## License

Images are sourced from YFCC15M under their original CC licenses (Attribution / Attribution-ShareAlike / Attribution-NonCommercial-NoDerivs). Code in this repository is released under the Apache License 2.0.