"""Sharpness, frozen VGG Gram features, and global LAB sensitivity controls."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from ..data.inventory import check_image
from ..models.embeddings import extract_visual, load_visual, save_array
from ..provenance import atomic_json, task_seed
from .evaluate import compute_trajectories, swd


def transfer(image, mean, std):
    import cv2

    lab = cv2.cvtColor(np.asarray(image, dtype=np.float32) / 255, cv2.COLOR_RGB2LAB)
    lab = (lab - lab.mean(axis=(0, 1))) / (lab.std(axis=(0, 1)) + 1e-9) * std + mean
    rgb = cv2.cvtColor(lab.astype(np.float32), cv2.COLOR_LAB2RGB)
    return Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))


def sampled_rows(meta, concept, b, count, seed):
    rows = meta[(meta.concept == concept) & (meta.temp_bin == b)].copy()
    rows["_rank"] = rows.image_id.map(lambda value: task_seed(seed, "style_sample", value))
    return rows.sort_values(["_rank", "image_id"]).head(count)


def style_controls(cfg, folder, inventory):
    import cv2
    import torch
    from torchvision import models, transforms

    from ..provenance import seed_process

    seed_process(cfg["seed"], torch_required=True)
    network = models.vgg16(weights=models.VGG16_Weights.IMAGENET1K_V1)
    vgg = network.features[:15].to(cfg["device"]).eval()
    for parameter in vgg.parameters():
        parameter.requires_grad_(False)
    preprocess = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    # Record the actual weight tensor bytes, not only its public download URL.
    import hashlib

    h = hashlib.sha256()
    for name, tensor in sorted(vgg.state_dict().items()):
        h.update(name.encode())
        h.update(tensor.detach().cpu().numpy().tobytes())
    atomic_json(
        folder / "vgg_weights.json",
        {"enum": "VGG16_Weights.IMAGENET1K_V1", "feature_state_sha256": h.hexdigest()},
    )
    rows = []
    b0, _, b2 = cfg["experiment"]["temporal_bins"]
    for concept in sorted(cfg["experiment"]["concepts"]):
        gram_pools, sharpness = [], []
        for b in (b0, b2):
            sample = sampled_rows(
                inventory, concept, b, cfg["style"]["sample_per_bin"], cfg["seed"]
            )
            images = [check_image(Path(cfg["data_root"]), row) for row in sample.itertuples()]
            if len(images) < 2:
                gram_pools.append(None)
                sharpness.append(float("nan"))
                continue
            sharpness.append(
                float(
                    np.mean(
                        [
                            cv2.Laplacian(
                                np.asarray(image.convert("L").resize((128, 128)), dtype=np.float32),
                                cv2.CV_32F,
                            ).var()
                            for image in images[: cfg["style"]["sharpness_sample"]]
                        ]
                    )
                )
            )
            grams = []
            with torch.inference_mode():
                for start in range(0, len(images), cfg["batch_size"]):
                    batch = torch.stack(
                        [preprocess(im) for im in images[start : start + cfg["batch_size"]]]
                    )
                    features = vgg(batch.to(cfg["device"]))
                    batch_size, channels, height, width = features.shape
                    features = features.reshape(batch_size, channels, height * width)
                    gram = torch.bmm(features, features.transpose(1, 2)) / (
                        channels * height * width
                    )
                    ix = torch.triu_indices(channels, channels, device=cfg["device"])
                    grams.append(gram[:, ix[0], ix[1]].cpu().numpy())
            pool = np.vstack(grams)
            gram_pools.append(pool)
            save_array(folder / f"gram-{concept}-{b}.npy", pool)
        rows.append(
            {
                "concept": concept,
                "style_swd": swd(cfg, *gram_pools)
                if all(p is not None for p in gram_pools)
                else np.nan,
                "delta_sharpness": sharpness[1] - sharpness[0],
            }
        )
        print(f"Style controls: {concept}", flush=True)
    pd.DataFrame(rows).to_csv(folder / "style_metrics.csv", index=False)


def normalized_visual(cfg, folder, inventory, original, taxonomy_path):
    import cv2

    # Streaming sufficient statistics avoid storing hundreds of millions of Python floats.
    sample = inventory.copy()
    sample["_rank"] = sample.image_id.map(lambda value: task_seed(cfg["seed"], "lab", value))
    sample = sample.sort_values(["_rank", "image_id"]).head(cfg["style"]["reference_images"])
    total = 0
    sums, squares = np.zeros(3), np.zeros(3)
    for row in sample.itertuples():
        image = check_image(Path(cfg["data_root"]), row).resize((128, 128))
        pixels = cv2.cvtColor(np.asarray(image, dtype=np.float32) / 255, cv2.COLOR_RGB2LAB).reshape(
            -1, 3
        )
        pixels = pixels.astype(np.float64)
        sums += pixels.sum(axis=0)
        squares += (pixels * pixels).sum(axis=0)
        total += len(pixels)
    mean = sums / total
    std = np.sqrt(np.maximum(squares / total - mean * mean, 0))
    atomic_json(
        folder / "lab_reference.json",
        {
            "mean": mean.tolist(),
            "std": std.tolist(),
            "image_ids": sample.image_id.tolist(),
            "pixels": total,
        },
    )
    sn_cfg = {
        **cfg,
        "experiment": {
            **cfg["experiment"],
            "models": {"clip": cfg["experiment"]["models"]["clip"]},
        },
    }
    extract_visual(sn_cfg, folder, inventory, transform=lambda image: transfer(image, mean, std))
    original_embs, meta = load_visual(original, "clip")
    normalized, sn_meta = load_visual(folder, "clip")
    if meta.image_id.tolist() != sn_meta.image_id.tolist():
        raise ValueError("Original and normalized image identities do not align")
    b0, _, b2 = cfg["experiment"]["temporal_bins"]
    splits = pd.read_csv(taxonomy_path / "splits.csv")
    test_ids = set(splits.loc[splits.split == "test", "image_id"])
    records = []
    test_records = []
    for concept in sorted(meta.concept.unique()):
        ix = [
            meta.index[(meta.concept == concept) & (meta.temp_bin == b)].to_numpy()
            for b in (b0, b2)
        ]
        if any(len(i) < 2 for i in ix):
            continue
        before, after = (
            swd(cfg, original_embs[ix[0]], original_embs[ix[1]]),
            swd(cfg, normalized[ix[0]], normalized[ix[1]]),
        )
        records.append(
            {
                "concept": concept,
                "vis_swd": before,
                "vis_swd_sn": after,
                "pct_retained_raw": 100 * after / before if before else np.nan,
            }
        )
        test_ix = [
            meta.index[
                (meta.concept == concept) & (meta.temp_bin == b) & meta.image_id.isin(test_ids)
            ].to_numpy()
            for b in (b0, b2)
        ]
        if all(len(i) >= 2 for i in test_ix):
            test_records.append(
                {
                    "concept": concept,
                    "vis_swd_sn_test": swd(cfg, normalized[test_ix[0]], normalized[test_ix[1]]),
                }
            )
    # Ratios are unbounded sensitivity measurements; no causal semantic percentages or clamping.
    pd.DataFrame(records).to_csv(folder / "normalization_sensitivity.csv", index=False)
    pd.DataFrame(test_records).to_csv(folder / "normalization_heldout.csv", index=False)
    compute_trajectories(sn_cfg, folder, folder, suffix="color_normalized")
