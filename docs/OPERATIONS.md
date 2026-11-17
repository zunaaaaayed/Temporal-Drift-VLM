# Remote operation with tmux

`tdrift run` starts a detached tmux worker outside tmux, and runs directly inside an
existing tmux session. Inference, fits, permutation tests, clustering, normalization
and UMAP execute there. Lightweight `validate`, `status` and `compare` need no session.

```bash
tmux list-sessions
tmux attach -t tdrift-study-001
# Ctrl-b d detaches. Disconnecting SSH also leaves the worker running.
tail -f runs/study-001/console.log
.venv/bin/tdrift status --config configs/research.json --run-id study-001
```

Detached workers write `exit_code.txt` when they finish; zero means success. Their
session normally disappears. `run.json` records stage state, artifact locations and
failures. A hard kill may leave status "running" until resumed; inspect the exit code
and log. Inside an existing interactive tmux session, output appears in that terminal.

To stop intentionally, attach and press Ctrl-c. Resume by repeating the exact run
command and run ID. tmux protects against SSH/terminal loss; it cannot protect against
server reboot, storage failure, OOM kills or scheduler termination. Checkpoints address
process interruption; backups address storage loss.

Use distinct IDs for different experiments. Artifact locks prevent simultaneous stage
writes; run locks prevent concurrent updates of one manifest. Do not clean active
artifact folders. Run on allocated compute resources according to institutional policy;
tmux does not allocate a GPU.

`bash scripts/bootstrap.sh research` installs the large optional environment inside
tmux. Research config explicitly selects CUDA, smoke explicitly selects CPU. Weight
downloads occur inside workers using checked-in immutable source revisions.
