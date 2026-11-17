# Reproducibility protocol

## What is fixed

- Direct and transitive versions and distribution hashes in `uv.lock`; use `--frozen`.
- Immutable model/dataset commits, including OpenCLIP's XLM-R config and tokenizer.
- Photograph bytes, SHA-256 image IDs, validation and duplicate ledger.
- Resolved experiment/prompt definitions, batch size, device, FP32, CPU thread limits.
- Hash seed before interpreter startup; task-local NumPy RNGs; strict deterministic
  PyTorch operations; disabled cuDNN benchmarking/TF32; cuBLAS workspace configuration.
- Stable input order and ranking ties, saved image-ID splits and permutation nulls.
- Package source, environment, dependency versions, GPU driver and inference runtime.
- A per-run copy of working package source and lockfile, even before a Git commit.
- Hashes of actual loaded model tensors, in addition to repository revisions.

PyTorch does not guarantee identical output across releases/platforms. This framework
targets and verifies exact repeated computation in the same recorded environment.
Sources: [PyTorch reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html),
[deterministic algorithms](https://docs.pytorch.org/docs/stable/generated/torch.use_deterministic_algorithms.html),
[sliced Wasserstein definitions](https://pythonot.github.io/gen_modules/ot.sliced.html).

## Run, resume, verify

1. Archive original image bytes and model snapshots. A pinned metadata revision does
   not freeze changing Flickr CDN contents or availability.
2. Commit source, configs and lockfile. Keep credentials outside version control.
3. Start through `tdrift run`; it uses tmux. The resolved config and environment are
   written under `runs/<id>/` before computation.
4. Back up `data/`, `artifacts/` and `runs/`. Output symlinks alone are not an archive.
5. To resume, repeat the same run ID, config, stage list and flags. Completed outputs
   are verified; visual batches resume from atomic numeric checkpoints. Other stages
   restart deterministically if incomplete.
6. To test independent recomputation, copy the config, change `artifact_root`, and use
   a new run ID. `tdrift compare` verifies files and compares all stage output hashes.
   Same-root repeats test cache reuse, not independent recomputation.

Completed artifacts are immutable. Corruption fails explicitly; preserve the affected
artifact for diagnosis and select a new artifact root. Do not edit cached results.
Changed source/config/environment requires a new run ID. Location changes alone do
not change scientific identity.

Source identity covers package code, pyproject and lockfile. Config identity expands
experiment, source and prompt files. Environment identity records Python, installed
packages, platform, CPU descriptor, GPU/driver and thread settings. Model stages also
record torch/CUDA/cuDNN versions, selected device, deterministic mode and precision.

## Limits

The framework performs pretrained inference and analysis, without training/fine-tuning.
Strict deterministic CUDA mode fails if an operation lacks a supported deterministic
implementation. Fix the environment or explicitly select CPU in a separate config;
there is no silent device fallback. Unknown historical dependencies and unavailable
original photographs prevent unconditional reproduction of old notebook numbers.

Reproducible weak-label drift remains weak-label drift. Validate image relevance,
uploader imbalance, near-duplicates, timestamps, translations, and concept overlap
before interpreting distribution changes as semantic evolution.
