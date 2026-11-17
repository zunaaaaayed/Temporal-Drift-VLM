"""Pinned metadata collection and restartable, verified downloads."""

from __future__ import annotations

import io
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests
from PIL import Image

from ..provenance import atomic_bytes, atomic_json, file_hash


def collect(cfg: dict, folder: Path) -> None:
    from datasets import load_dataset
    source = cfg["sources"]["dataset"]
    e = cfg["experiment"]
    patterns = {c: re.compile(rf"\b{re.escape(c)}\b", re.IGNORECASE) for c in e["concepts"]}
    quotas = {(c, b): 0 for c in e["concepts"] for b in e["temporal_bins"]}
    path = folder / "metadata.jsonl"
    records = {}
    if path.exists():
        lines = path.read_text().splitlines()
        for index, line in enumerate(lines):
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                if index != len(lines)-1:
                    raise
                break  # A hard kill may tear only the final append.
            records[row["photo_id"]] = row
            quotas[row["concept"], row["temp_bin"]] += 1
        atomic_bytes(path, b"".join((json.dumps(r, ensure_ascii=False)+"\n").encode()
                                  for r in records.values()))
    stream = load_dataset(source["repo"], revision=source["revision"], split="train", streaming=True)
    for index, row in enumerate(stream):
        photo_id = str(row.get("photoid", ""))
        if not photo_id or photo_id in records:
            continue
        try:
            year = int(str(row.get("datetaken", ""))[:4])
        except ValueError:
            continue
        if not 2004 <= year <= 2014:
            continue
        b = e["temporal_bins"][0 if year < 2008 else 1 if year <= 2011 else 2]
        text = f"{row.get('title', '')} {row.get('description', '')}"
        for concept in e["concepts"]:
            if quotas[concept, b] >= e["target_per_bin"] or not patterns[concept].search(text):
                continue
            url = str(row.get("downloadurl", "")).replace("http://", "https://", 1)
            if not url.startswith("https://"):
                continue
            record = {"photo_id": photo_id, "concept": concept, "temp_bin": b,
                      "year": year, "url": url, "uploader": str(row.get("uid", "")),
                      "title": str(row.get("title", "")),
                      "license": str(row.get("licensename", ""))}
            records[photo_id] = record
            quotas[concept, b] += 1
            # A completed line is a restart point; a torn last line is handled below.
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                handle.flush()
            break
        if index % 100000 == 0:
            print(f"metadata scan: {index:,} rows; {len(records):,} selected", flush=True)
        if all(n >= e["target_per_bin"] for n in quotas.values()):
            break
    if not records:
        raise ValueError("No matching metadata found")
    atomic_bytes(path, b"".join((json.dumps(r, ensure_ascii=False) + "\n").encode()
                              for r in sorted(records.values(), key=lambda r: r["photo_id"])))
    atomic_json(folder / "coverage.json", {f"{c}/{b}": n for (c, b), n in quotas.items()})


def download(cfg: dict, folder: Path, metadata: Path) -> None:
    rows = [json.loads(line) for line in metadata.read_text().splitlines()]
    root = Path(cfg["data_root"])
    ledger_path = folder / "downloads.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}

    def one(row):
        pid = row["photo_id"]
        if not re.fullmatch(r"[A-Za-z0-9_-]+", pid):
            raise ValueError("Invalid photo ID")
        dest = root / "images" / row["concept"] / row["temp_bin"] / f"{pid}.jpg"
        if dest.exists():
            sha = file_hash(dest)
            if pid in ledger and "sha256" in ledger[pid] and sha != ledger[pid]["sha256"]:
                raise ValueError(f"Downloaded file mutated: {dest}")
            with Image.open(dest) as image:
                image.verify()
            return pid, {"path": dest.relative_to(root).as_posix(), "sha256": sha,
                         "url": row["url"], "origin": ledger.get(pid, {}).get("origin", "existing_local")}
        if pid in ledger and "sha256" in ledger[pid]:
            raise ValueError(f"Previously downloaded bytes missing: {dest}; restore the archived file")
        try:
            response = requests.get(row["url"], timeout=(10, 30))
            response.raise_for_status()
            with Image.open(io.BytesIO(response.content)) as img:
                img.verify()
            atomic_bytes(dest, response.content)
            return pid, {"path": dest.relative_to(root).as_posix(), "sha256": file_hash(dest),
                         "url": row["url"], "origin": "download"}
        except (requests.RequestException, OSError) as exc:
            return pid, {"error": str(exc), "url": row["url"]}

    with ThreadPoolExecutor(max_workers=cfg["download_workers"]) as pool:
        for i, (pid, result) in enumerate(pool.map(one, rows), 1):
            ledger[pid] = result
            if i % 100 == 0:
                atomic_json(ledger_path, ledger)
                print(f"downloads: {i}/{len(rows)}", flush=True)
    atomic_json(ledger_path, ledger)
    pd.DataFrame([{**row, **ledger[row["photo_id"]]} for row in rows]).to_csv(
        folder / "downloads.csv", index=False)
