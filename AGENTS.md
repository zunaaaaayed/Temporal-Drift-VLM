# Research repository conventions

- Run model inference, statistical fitting, clustering, UMAP, experiments and fitting
  integration tests inside tmux. Use `tdrift run` or `bash scripts/checks.sh`.
  Read-only inspection and small pure metric checks may run directly.
- Preserve the 48-concept notebook and draft PDF as historical inputs.
- Never edit completed artifacts or hard-code manuscript numbers into reports.
- Document methodological changes in `docs/MIGRATION.md`; numerical discrepancies
  are provenance questions, not targets to force into passing tests.
- Use stable image IDs, immutable source revisions, local RNGs, aligned metadata,
  explicit split provenance and validated caches.
- Do not silently weaken deterministic settings or switch devices after failure.
- Verify with `bash scripts/checks.sh`, including independent synthetic recomputation.
- Do not commit raw data, weights, credentials, runtime logs, embeddings or large
  artifact caches. Scientific reports, tables, figures and run provenance explicitly
  allowed by .gitignore may be versioned.
