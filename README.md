# Temporal Drift in Visual Embedding Spaces

A modular research framework for temporal probing of frozen multilingual
vision-language models. The reference experiment covers 48 concepts, six languages,
three periods (2004–2007, 2008–2011, 2012–2014), and CLIP, multilingual OpenCLIP,
and SigLIP-2.

**Authors:** Md Zunayedul Islam and Dr. Marcos Escudero-Viñolo,
Universidad Autónoma de Madrid.

The original 48-concept notebook (`t-Drift-VLM_48c.ipynb`) is preserved locally as a
historical record and excluded from Git. Its saved results and the draft paper disagree
in several places. The package
generates results from versioned inputs. See [migration and scientific changes](docs/MIGRATION.md).

## Quick start

Requirements: Linux, `tmux`, and [uv](https://docs.astral.sh/uv/getting-started/installation/).
Python 3.11.12 is the reference interpreter; the core also supports 3.12–3.13.
`uv.lock` pins direct and transitive dependencies, including optional model libraries.

```bash
# Installation continues inside tmux. Wait for its log to say Environment ready.
bash scripts/bootstrap.sh core
.venv/bin/tdrift validate
.venv/bin/tdrift smoke --run-id smoke
```

Smoke creates a tiny, explicitly synthetic corpus and starts the complete core pipeline
in tmux. It downloads no models and produces no scientific VLM claims.

```bash
tmux attach -t tdrift-smoke
# Detach without stopping: Ctrl-b, then d
.venv/bin/tdrift status --config runs/smoke-fixture/smoke.json --run-id smoke
```

The session exits on completion; its logs, manifest and exit code remain on disk.
SSH disconnection leaves the worker running while the server remains alive.

## Research runs

```bash
bash scripts/bootstrap.sh research
```

Place archived photographs under `data/images/{concept}/{temporal_bin}/`, or copy
`configs/research.json` within `configs/` and change `data_root` to your existing
corpus directory. Paths are relative to the configuration file. An existing notebook
data directory should contain `images/{concept}/{temporal_bin}/*.jpg`. PNG/JPEG are
supported. Unversioned notebook embedding caches are not silently reused.

```bash
.venv/bin/tdrift run \
  --config configs/research.json --run-id study-001 \
  --with-style --stages plots grids projections
```

This automatically launches a detached tmux worker. Inside tmux it runs there directly.
Dependencies run in order. The full workflow includes validation, visual/text embeddings,
held-out taxonomy, drift, retrieval, trajectory nulls, sharpness/VGG controls,
colour-normalized CLIP embeddings, statistics, UMAP/PCA, and retrieval grids.

```bash
# Core experiment, omitting expensive photographic controls and UMAP:
.venv/bin/tdrift run \
  --config configs/research.json --run-id core-001

# Resume after interruption: repeat the identical command and run ID.
# Changed experiment: use a new configuration and a new run ID.
.venv/bin/tdrift stages
.venv/bin/tdrift status --config configs/research.json --run-id study-001
```

For new data collection from the pinned YFCC metadata source:

```bash
.venv/bin/tdrift run \
  --config configs/research.json --run-id collection-001 --stages download inventory
```

Flickr availability changes. Archive actual image bytes, inventory, metadata and model
snapshots. A repeated download is not a substitute for that archive. Keyword labels
are weak labels and still require visual validation.

## Organization

```text
configs/                       Experiment, prompts, immutable source revisions
src/temporal_drift/
  cli.py                       tmux, status, config validation, result comparison
  pipeline.py                  Stage dependencies and durable run lifecycle
  config.py                    Configuration validation
  provenance.py                Hashes, atomic persistence, environment and seeds
  artifacts.py                 Content-addressed artifacts, locks, integrity checks
  data/                        Metadata, downloads, image inventories, synthetic fixture
  models/                      Model adapters, prompts, checkpointed inference
  metrics/                     SWD, geometry, AP, permutation trajectory nulls
  analysis/                    Taxonomy, evaluation, statistics, photographic controls
  visualization/               Figures, UMAP/PCA, auditable retrieval grids
scripts/                       tmux-based setup and verification
tests/                         Numerical and independent end-to-end tests
docs/                          Migration, reproducibility and operations
doc/                           Draft paper; archived notebook-era README
data/                          Local corpus (ignored)
artifacts/                     Versionable reports/tables/figures; large caches ignored
runs/                          Versionable provenance/source snapshots; logs/work data ignored
```

## Outputs

Every run stores `config.resolved.json` and `run.json`: source hashes, exact packages,
model revisions, environment, hardware, input identities, output hashes and stage state.
`runs/<id>/outputs/` links to immutable stage directories.
`.gitignore` permits scientific reports, tables, figures, manifests, launch commands
and frozen source snapshots to be versioned. Images, model weights, embedding arrays,
runtime logs and working caches remain local and require separate backups.

| Stage | Principal outputs |
|---|---|
| inventory | Image IDs, SHA-256, paths; corrupt/duplicate rejection ledger |
| embed/text | Numeric arrays with aligned image/prompt metadata |
| taxonomy | Image-ID splits, proxy/test SWD, tertile and k-means labels |
| metrics | Full and genuinely held-out visual/retrieved drift tables |
| trajectory | Angles, concept-specific permutation null arrays |
| retrieval | Corrected AP, labeled legacy AP, precision, random expectations |
| statistics | `tests.json`, fit diagnostics, regimes, ICC, generated `REPORT.md` |
| normalize | LAB reference, normalized embeddings, raw sensitivity ratios, H3 |
| plots/grids/projections | Figures, retrieved image IDs, UMAP/PCA arrays |

Verify independent computation by copying the config, changing `artifact_root`,
and running with a new ID. Then:

```bash
.venv/bin/tdrift compare runs/study-001 runs/study-002
```

This verifies actual artifact files and compares all output hashes. Reusing the same
artifact root tests cache reuse; a fresh root tests recomputation. Exact equality is
a verifiable same-environment target, not an unconditional cross-hardware promise.
See the [reproducibility protocol](docs/REPRODUCIBILITY.md).

## Verification

```bash
bash scripts/checks.sh
```

Checks run inside tmux. They cover independent synthetic reruns, corrected AP,
unequal-sample transport, image-ID split disjointness, cache corruption/invalidation,
and interrupted-stage resume. Real scientific runs additionally require model weights
and the archived corpus; the synthetic suite does not validate actual VLM inference.
The separate real-weight adapter check and completed verification runs are documented
in [VALIDATION.md](docs/VALIDATION.md).

Licensed under [Apache 2.0](LICENSE).
