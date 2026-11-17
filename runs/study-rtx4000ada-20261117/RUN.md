# Active full experiment

Launched 2026-11-17T02:57:58.821422+01:00 (Europe/Paris).

- Device: NVIDIA RTX 4000 Ada Generation, CUDA, FP32.
- Config: `configs/rtx4000ada-20261117.json`; seed 42; eight CPU threads; batch 48; 16 download workers.
- Scope: 48 concepts, six languages, three periods, all three models. Target: up to 400 metadata matches per concept/bin.
- Source: pinned YFCC15M commit; this is a new image snapshot, not the unavailable original corpus.
- Main tmux: `tdrift-study-rtx4000ada-20261117`.
- Early-download tmux: `tdrift-study-prefetch-20261117`; downloads roughly the first 4,000 selected photos, sharing the final downloader's image-write lock.
- GPU text run: `study-rtx4000ada-20261117-text` (currently complete); its immutable outputs are reused by the main run.
- Data: `data/yfcc15m-20261117/images/`.
- Artifacts: `artifacts/rtx4000ada-20261117/`.

The main job runs collection, final download, inventory, embeddings, taxonomy, metrics, trajectories, retrieval, VGG controls, colour-normalized CLIP, statistics, plots, UMAP/PCA and qualitative grids. Image inventory is frozen only after the final download pass. Failed URLs are recorded.

## Monitoring

From the repository root:

```bash
.venv/bin/tdrift status --config configs/rtx4000ada-20261117.json --run-id study-rtx4000ada-20261117
tail -f runs/study-rtx4000ada-20261117/console.log
tmux attach -t tdrift-study-rtx4000ada-20261117
```

Detach with Ctrl-b, then d. Closing SSH does not stop tmux. Logs, manifests and checkpoints persist. Do not edit the package while this run is active: the source-integrity guard rejects mixed-source computation.

To resume the same frozen-code run after an interruption, execute `bash runs/study-rtx4000ada-20261117/launch.sh` inside tmux. The script preserves the exact stage list and flags.
