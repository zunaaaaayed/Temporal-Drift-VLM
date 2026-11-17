# Verification record

Verified on 2026-11-17 using the locked Python 3.11.12 environment, on CPU.
All inference, fitting and integration runs executed inside tmux.

| Check | Result |
|---|---|
| Ruff lint and formatting | Passed |
| Shell syntax | Passed |
| Unit and integration suite | 15 passed |
| Independent core synthetic reruns | Every artifact output hash identical |
| Extended synthetic experiment | All 13 stages completed |
| Independent extended rerun | All 13 stages' output hashes identical |
| Real CLIP + multilingual text adapter | Passed; image 1×512, text 3×512 |
| Real multilingual OpenCLIP adapter | Passed; image 1×512, text 3×512 |
| Real SigLIP-2 adapter | Passed; image 1×768, text 3×768 |
| Repeated real-weight CPU inference | Arrays exactly equal; unit norms verified |
| Source distribution and wheel build | Passed |

The automated suite covers corrected AP and gallery-specific random expectations,
exact unequal-sample transport, deterministic permutation nulls, stable disjoint splits,
invalid/duplicate image handling, failed-batch resume, immutable run IDs, cache
invalidation/corruption, source snapshots, and the tmux execution requirement.

The extended experiment uses 216 generated images (six concepts × three bins × 12),
synthetic embedding adapters, and the real pretrained VGG-16 style network. It exercises
sharpness/style controls, LAB normalization, held-out normalized comparisons, statistical
models, figures, retrieval grids, UMAP and PCA. It contains no scientific VLM findings.

The separate real-model check uses pinned actual weights, one generated image, and
English/Bengali/Japanese text queries for each adapter. It verifies the real loading APIs,
visual/text embedding dimensions, normalization, and exact repeated inference. It does
not establish retrieval quality or reproduce the historical research corpus.

Local evidence (logs stay ignored; reports, manifests and source snapshots may be versioned):

- `runs/verification/checks-release.log`
- `runs/model-adapter-check/results.json` and `verified.json`
- `runs/verification/model-adapters-v2.log`
- `runs/verification/extended-repeat.log`
- `runs/extended-fixture/runs/extended/run.json`
- `runs/extended-fixture/runs/extended-repeat/run.json`

The original 49,304-image corpus is absent from this checkout. The initial restricted
execution environment could not access NVIDIA, so those checks used CPU. A subsequent
host-level check confirmed a working RTX 4000 Ada Generation (20,475 MiB), driver
620.70.06, and CUDA availability in PyTorch 2.7.1+cu126. The scientific run collects a
new pinned-source snapshot; it cannot reproduce unavailable historical image bytes.

The final changes after the extended comparison add CPU model/features to provenance
and enforce tmux for direct pipeline calls. The 15-test suite, including independent
core recomputation, was rerun after those changes.
