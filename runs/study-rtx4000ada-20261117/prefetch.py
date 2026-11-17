"""Download up to 4,000 selected photos early, before the metadata scan ends.

The package downloader serializes image writes with the final download pass.
The primary pipeline freezes/validates its inventory only after that final pass.
"""
import json
import os
import time
from pathlib import Path
from temporal_drift.config import load_config
from temporal_drift.data.collect import download
from temporal_drift.provenance import atomic_bytes, atomic_json

if not os.environ.get('TMUX'):
    raise SystemExit('Run inside tmux')
cfg=load_config('configs/rtx4000ada-20261117.json')
run=Path(cfg['run_root'])/'study-rtx4000ada-20261117'
seen=set()
batch_number=0
successes=0
errors=0
while len(seen)<4000:
    manifest_path=run/'run.json'
    if not manifest_path.exists():
        time.sleep(2)
        continue
    manifest=json.loads(manifest_path.read_text())
    stage=manifest['stages'].get('collect',{})
    if manifest['status']=='failed':
        raise RuntimeError(manifest.get('error','Primary run failed'))
    if stage.get('status')=='complete':
        print('Metadata collection finished; handing image writes to final download stage.',flush=True)
        break
    if 'key' not in stage:
        time.sleep(2)
        continue
    metadata=Path(cfg['artifact_root'])/'collect'/stage['key']/'metadata.jsonl'
    if not metadata.exists():
        time.sleep(2)
        continue
    pending=[]
    for line in metadata.read_text(encoding='utf-8').splitlines():
        try:
            row=json.loads(line)
        except json.JSONDecodeError:
            continue
        if row['photo_id'] not in seen:
            pending.append(row)
        if len(pending)==100:
            break
    if not pending:
        time.sleep(2)
        continue
    batch=run/'prefetch'/f'{batch_number:05d}'
    batch.mkdir(parents=True,exist_ok=True)
    snapshot=batch/'metadata.jsonl'
    atomic_bytes(snapshot,b''.join((json.dumps(row)+'\n').encode() for row in pending))
    download(cfg,batch,snapshot)
    ledger=json.loads((batch/'downloads.json').read_text())
    successes+=sum('sha256' in value for value in ledger.values())
    errors+=sum('error' in value for value in ledger.values())
    seen.update(row['photo_id'] for row in pending)
    batch_number+=1
    atomic_json(run/'prefetch_summary.json',{'attempted':len(seen),'downloaded':successes,'failed':errors,'batches':batch_number})
    print(f'Prefetch: {len(seen)} attempted; {successes} downloaded; {errors} failed.',flush=True)
print('Early download worker finished.',flush=True)
