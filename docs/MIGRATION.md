# Notebook migration and scientific protocol

The original 48-concept notebook remains unchanged. `doc/legacy/README.notebook.md`
preserves its previous README. `configs/experiment.notebook.json` and
`configs/prompts.notebook.json` were extracted from cells 7 and 23. These are
historical references, not endorsements of every interpretation in their prose.

## Section mapping

| Notebook section | Implementation |
|---|---|
| Environment, configuration, reproducibility | `config.py`, `provenance.py`, `pyproject.toml`, `uv.lock` |
| I: metadata/downloads/embeddings | `data/collect.py`, `data/inventory.py`, `models/embeddings.py` |
| II: prompts and text encoders | `models/prompts.py`, `models/encoders.py`, prompt JSON |
| III: metrics/model comparison | `metrics/distribution.py`, `analysis/evaluate.py`, `analysis/statistics.py` |
| IV: trajectories | `metrics/trajectory.py`, `analysis/evaluate.py` |
| V: taxonomy | `analysis/taxonomy.py` |
| VI: hypothesis tests | `analysis/statistics.py` |
| VII–VIII: photographic controls | `analysis/style.py` |
| IX: retrieval quality | `metrics/retrieval.py`, `analysis/evaluate.py` |
| X: figures, UMAP, PCA | `visualization/plots.py` |
| XI: qualitative grids | `visualization/plots.py::retrieval_grids` (active, saved image IDs) |

## Deliberate scientific changes

These corrections change results. The package does not claim to regenerate exact
historical values from the notebook's unrecorded software/data environment.

1. **Explicit SWD order.** The notebook POT call implicitly used p=2 despite its W1
   markdown. Default config preserves p=2. Exact empirical quantile integration
   handles unequal cloud sizes. Gram SWD now uses the same explicit order, replacing
   the separate interpolated-W1 helper.
   VGG uses the original `features[:15]` slice; this ends at `conv3_3` in torchvision,
   despite the notebook's comment calling it `relu3_1`.
2. **Content-based image identity.** Invalid images are rejected before inference.
   Identical bytes are globally deduplicated in deterministic concept/bin order;
   cross-label duplicates remain visible in the rejection ledger.
3. **Stable, disjoint splits.** Hash-ranked image IDs assign half of each eligible bin
   to labeling and the rest to test. Each half needs at least two images. Fixed 200-row
   cuts previously left sparse concepts without test images.
4. **Balanced tertiles.** Group sizes differ by at most one. Unobserved concepts have
   no fabricated empirical tier. The historical 15/15/17 split is not carried forward.
5. **Actual held-out retrieval.** Test top-k pools and retrieved SWD are recomputed
   from test images. H1 regressions do not reuse full-pool retrieval results.
6. **Independent comparisons.** Independent-label permutations retain unequal group
   sizes, replacing arbitrary pairing/truncation. Raw and Holm-adjusted contrast
   p-values are reported. Resource predictors are centered before interactions.
7. **H2 inference unit.** The pooled correlation is descriptive. Exact permutation
   inference uses the six language means. Repeating M-CLIP drift across visual models
   does not create independent text-encoder replications. Morphology is not tested
   causally by this protocol.
8. **Corrected AP.** Normalize by min(total relevant gallery images, k). Keep
   `legacy_AP` explicitly labeled. Calculate random expectations from actual gallery
   size and concept prevalence, rather than using 1/concept_count as MAP.
9. **Consistent trajectory geometry.** Observed and permuted centroids use identical
   normalization. Seeds are local to concept/model; all null angles are saved.
10. **Colour normalization as sensitivity.** Retain ratios above 100%; do not clamp
    or interpret the remainder as a causal semantic percentage. Reports are generated
    from measured values and fit diagnostics, not manuscript text.
11. **Validated caches.** Source, config, environment and input identities determine
    stage identities. Reuse verifies every output hash. Legacy pickled caches are not
    trusted or imported automatically.

## Prompt caveats

Original wording is preserved, including the Arabic late-period wording and
translations needing native-speaker review. Put reviewed replacements in a new
prompt JSON and config/run; changed text invalidates dependent artifacts. Japanese
concept nouns remain fixed across periods, so temporal-prompt displacement alone
does not demonstrate lexical substitution.

## Historical disagreements with the paper

The draft's W=0 claims differ from saved W=27 (original) and W=46 (normalized).
Its data-driven fast-interaction p=0.0004 differs from saved p=0.0535. Its taxonomy
table does not follow its tertile definition, and retrieval language entries do not
average to the printed model averages. Some figures preserve correct notebook outputs.
Treat the PDF as a historical draft containing mixed revisions.
