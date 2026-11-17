"""Dependency-aware pipeline with immutable artifacts and durable run status."""

from __future__ import annotations

import copy
import json
import logging
import os
import traceback
from pathlib import Path

from .artifacts import build, exclusive_lock
from .config import scientific_config
from .provenance import (
    atomic_json,
    digest,
    environment,
    now,
    seed_process,
    source_fingerprint,
    snapshot_source,
)

DEPENDENCIES = {
    "collect": [],
    "download": ["collect"],
    "inventory": [],
    "embed": ["inventory"],
    "text": [],
    "taxonomy": ["embed"],
    "metrics": ["embed", "text", "taxonomy"],
    "trajectory": ["embed"],
    "retrieval": ["embed", "text"],
    "style": ["inventory"],
    "normalize": ["inventory", "embed", "taxonomy"],
    "statistics": ["metrics", "taxonomy", "trajectory"],
    "plots": ["metrics", "taxonomy", "trajectory", "retrieval", "statistics"],
    "projections": ["embed"],
    "grids": ["embed", "text"],
}
DEFAULT_STAGES = ["metrics", "trajectory", "retrieval", "statistics", "plots", "grids"]


def resolve_stages(requested, *, with_style=False):
    dependencies = copy.deepcopy(DEPENDENCIES)
    if with_style:
        dependencies["statistics"] += ["style", "normalize"]
        dependencies["plots"] += ["style", "normalize"]
    if "download" in requested:
        dependencies["inventory"] = ["download"]
    result = []

    def visit(name):
        if name not in dependencies:
            raise ValueError(f"Unknown stage {name}; choose from {', '.join(dependencies)}")
        for dependency in dependencies[name]:
            visit(dependency)
        if name not in result:
            result.append(name)

    for stage in requested:
        visit(stage)
    return result, dependencies


def execute_stage(name, cfg, folder, paths, inventory):
    if name == "collect":
        from .data.collect import collect

        collect(cfg, folder)
    elif name == "download":
        from .data.collect import download

        download(cfg, folder, paths["collect"] / "metadata.jsonl")
    elif name == "inventory":
        from .data.inventory import write_inventory

        write_inventory(folder, *inventory)
    elif name == "embed":
        from .models.embeddings import extract_visual

        extract_visual(cfg, folder, inventory[0])
    elif name == "text":
        from .models.embeddings import extract_text

        extract_text(cfg, folder)
    elif name == "taxonomy":
        from .analysis.taxonomy import fit_taxonomy
        from .models.embeddings import load_visual

        fit_taxonomy(cfg, folder, *load_visual(paths["embed"], "clip"))
    elif name == "metrics":
        from .analysis.evaluate import compute_metrics

        compute_metrics(cfg, folder, paths["embed"], paths["text"], paths["taxonomy"])
    elif name == "trajectory":
        from .analysis.evaluate import compute_trajectories

        compute_trajectories(cfg, folder, paths["embed"])
    elif name == "retrieval":
        from .analysis.evaluate import evaluate_retrieval

        evaluate_retrieval(cfg, folder, paths["embed"], paths["text"])
    elif name == "style":
        from .analysis.style import style_controls

        style_controls(cfg, folder, inventory[0])
    elif name == "normalize":
        from .analysis.style import normalized_visual

        normalized_visual(cfg, folder, inventory[0], paths["embed"], paths["taxonomy"])
    elif name == "statistics":
        from .analysis.statistics import analyze

        analyze(
            cfg,
            folder,
            paths["metrics"],
            paths["taxonomy"],
            paths["trajectory"],
            paths.get("style"),
            paths.get("normalize"),
        )
    elif name == "plots":
        from .visualization.plots import plot_results

        plot_results(cfg, folder, paths)
    elif name == "projections":
        from .visualization.plots import projections

        projections(cfg, folder, paths["embed"])
    elif name == "grids":
        from .visualization.plots import retrieval_grids

        retrieval_grids(cfg, folder, paths["embed"], paths["text"])
    else:
        raise ValueError(name)


def run(cfg, run_id, requested, *, with_style=False):
    stages, dependencies = resolve_stages(requested, with_style=with_style)
    if set(stages) - {"inventory"} and not os.environ.get("TMUX"):
        raise RuntimeError("Computation must run inside tmux; launch with tdrift run")
    seed_process(cfg["seed"])
    run_dir = Path(cfg["run_root"]) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    env = environment()
    science = scientific_config(cfg)
    # Ignore git dirtiness for the computational identity; actual source bytes are hashed.
    env_identity = {k: v for k, v in env.items() if k not in {"git_head", "git_status"}}
    identity = {"config": science, "source": source_fingerprint(), "environment": env_identity}
    signature = digest(identity)
    with exclusive_lock(run_dir / ".run.lock"):
        manifest_path = run_dir / "run.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text())
            if manifest["signature"] != signature or manifest["requested_stages"] != stages:
                raise ValueError(
                    "Run ID already belongs to different code, environment, or configuration; use a new ID"
                )
        else:
            manifest = {
                "schema": 1,
                "run_id": run_id,
                "signature": signature,
                "synthetic": cfg["synthetic"],
                "created_at": now(),
                "requested_stages": stages,
                "config": cfg,
                "environment": env,
                "source_fingerprint": identity["source"],
                "stages": {},
            }
            atomic_json(run_dir / "config.resolved.json", cfg)
            snapshot_source(run_dir / "source")
        manifest.update(status="running", updated_at=now())
        atomic_json(manifest_path, manifest)
        paths, records, inventory = {}, {}, None
        try:
            for name in stages:
                if source_fingerprint() != identity["source"]:
                    raise ValueError(
                        "Source changed during the run; preserve this run and start a new ID"
                    )
                if name == "inventory":
                    from .data.inventory import scan_images

                    inventory = scan_images(cfg)
                stage_identity = {
                    **identity,
                    "stage": name,
                    "dependencies": {d: records[d]["key"] for d in dependencies[name]},
                }
                if name == "inventory":
                    stage_identity["images"] = inventory[0].to_dict("records")
                    stage_identity["rejected"] = inventory[1]
                key = digest(stage_identity)
                previous_key = manifest["stages"].get(name, {}).get("key")
                if previous_key and previous_key != key:
                    raise ValueError(
                        f"Inputs for {name} changed; use a new run ID to preserve the old record"
                    )
                manifest["stages"][name] = {"status": "running", "started_at": now(), "key": key}
                atomic_json(manifest_path, manifest)
                logging.info("Stage %s", name)

                def compute(folder):
                    execute_stage(name, cfg, folder, paths, inventory)
                    if source_fingerprint() != identity["source"]:
                        raise ValueError(
                            "Source changed while computing a stage; no artifact was committed"
                        )

                path, record = build(Path(cfg["artifact_root"]), name, stage_identity, compute)
                # External image bytes are rehashed on every run by inventory; downloaded files
                # are also checked there before any downstream artifact is reused.
                paths[name], records[name] = path, record
                manifest["stages"][name] = {
                    "status": "complete",
                    "artifact": str(path),
                    "key": record["key"],
                    "completed_at": now(),
                    "outputs": record["outputs"],
                }
                atomic_json(manifest_path, manifest)
            if inventory is not None:
                from .data.inventory import scan_images

                final_inventory = scan_images(cfg)
                if (
                    not final_inventory[0].equals(inventory[0])
                    or final_inventory[1] != inventory[1]
                ):
                    raise ValueError(
                        "Image corpus changed during computation; archive a stable snapshot and rerun"
                    )
            manifest.update(status="complete", completed_at=now())
            outputs = run_dir / "outputs"
            outputs.mkdir(exist_ok=True)
            for name, path in paths.items():
                link = outputs / name
                if link.is_symlink():
                    link.unlink()
                if not link.exists():
                    link.symlink_to(path, target_is_directory=True)
            logging.info("Complete: %s", run_dir)
        except BaseException as exc:
            manifest.update(
                status="failed", failed_at=now(), error=str(exc), traceback=traceback.format_exc()
            )
            raise
        finally:
            atomic_json(manifest_path, manifest)
    return run_dir
