"""Library-specific calls isolated from experiment logic; weights use immutable revisions."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from ..metrics.distribution import normalize
from ..provenance import seed_process, task_seed


class Encoder:
    def __init__(self, cfg, key):
        import torch
        from huggingface_hub import snapshot_download
        from transformers import AutoModel, AutoProcessor, CLIPModel, CLIPProcessor

        seed_process(cfg["seed"], torch_required=True)
        if cfg["device"] == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA requested but unavailable; choose device=cpu explicitly")
        self.key, self.device = key, cfg["device"]
        source = cfg["sources"][key]
        self.text_model = None
        if key == "clip":
            self.processor = CLIPProcessor.from_pretrained(
                source["repo"], revision=source["revision"], use_fast=False
            )
            self.model = CLIPModel.from_pretrained(
                source["repo"], revision=source["revision"], attn_implementation="eager"
            )
            self.text_source = cfg["sources"]["mclip"]
        elif key == "m_openclip":
            import open_clip
            from open_clip.tokenizer import HFTokenizer

            local = snapshot_download(
                source["repo"],
                revision=source["revision"],
                allow_patterns=["open_clip_pytorch_model.bin"],
            )
            xlm = cfg["sources"]["xlm_roberta"]
            tokenizer_dir = snapshot_download(
                xlm["repo"],
                revision=xlm["revision"],
                allow_patterns=[
                    "config.json",
                    "tokenizer*",
                    "sentencepiece*",
                    "special_tokens_map.json",
                ],
            )
            architecture = "xlm-roberta-base-ViT-B-32"
            text_cfg = open_clip.get_model_config(architecture)["text_cfg"]
            text_cfg.update(
                hf_model_name=tokenizer_dir,
                hf_tokenizer_name=tokenizer_dir,
                hf_model_pretrained=False,
            )
            self.model, _, self.processor = open_clip.create_model_and_transforms(
                architecture,
                pretrained=str(Path(local) / "open_clip_pytorch_model.bin"),
                pretrained_hf=False,
                text_cfg=text_cfg,
            )
            self.tokenizer = HFTokenizer(
                tokenizer_dir, context_length=text_cfg.get("context_length", 77)
            )
        elif key == "siglip2":
            self.processor = AutoProcessor.from_pretrained(
                source["repo"], revision=source["revision"], use_fast=False
            )
            self.model = AutoModel.from_pretrained(
                source["repo"], revision=source["revision"], attn_implementation="eager"
            )
        else:
            raise ValueError(key)
        self.model = self.model.to(self.device).eval()

    def runtime(self):
        import torch

        fingerprints = {}
        for name, network in [
            ("visual_and_native_text", self.model),
            ("multilingual_text", self.text_model),
        ]:
            if network is None:
                continue
            hasher = hashlib.sha256()
            for parameter_name, parameter in sorted(network.state_dict().items()):
                hasher.update(parameter_name.encode())
                hasher.update(parameter.detach().cpu().contiguous().numpy().tobytes())
            fingerprints[name] = hasher.hexdigest()
        return {
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "cudnn": torch.backends.cudnn.version(),
            "device": self.device,
            "device_name": torch.cuda.get_device_name() if self.device == "cuda" else "CPU",
            "deterministic": torch.are_deterministic_algorithms_enabled(),
            "precision": "float32",
            "weight_state_sha256": fingerprints,
        }

    def images(self, images):
        import torch

        with torch.inference_mode():
            if self.key == "m_openclip":
                inputs = torch.stack([self.processor(image) for image in images]).to(self.device)
                result = self.model.encode_image(inputs)
            else:
                inputs = self.processor(images=images, return_tensors="pt").to(self.device)
                result = self.model.get_image_features(**inputs)
            return normalize(result.detach().cpu().float().numpy()).astype(np.float32)

    def texts(self, texts):
        import torch

        with torch.inference_mode():
            if self.key == "clip":
                if self.text_model is None:
                    from sentence_transformers import SentenceTransformer

                    self.text_model = SentenceTransformer(
                        self.text_source["repo"],
                        revision=self.text_source["revision"],
                        device=self.device,
                    )
                    self.text_model.eval()
                return self.text_model.encode(
                    texts, normalize_embeddings=True, show_progress_bar=False
                ).astype(np.float32)
            if self.key == "m_openclip":
                result = self.model.encode_text(self.tokenizer(texts).to(self.device))
            else:
                inputs = self.processor(
                    text=texts,
                    padding="max_length",
                    max_length=64,
                    truncation=True,
                    return_tensors="pt",
                ).to(self.device)
                result = self.model.get_text_features(**inputs)
            return normalize(result.detach().cpu().float().numpy()).astype(np.float32)


class SyntheticEncoder:
    """Deterministic CPU fixture; never presented as a scientific VLM result."""

    def __init__(self, cfg, key):
        self.cfg, self.key = cfg, key
        self.dimension = cfg["synthetic_dimension"]

    def images(self, images):
        projection = np.random.default_rng(task_seed(self.cfg["seed"], self.key)).normal(
            size=(48, self.dimension)
        )
        vectors = []
        for image in images:
            pixels = np.asarray(image.resize((4, 4)), dtype=float).reshape(-1) / 255
            vectors.append(pixels @ projection + 0.01)
        return normalize(np.stack(vectors)).astype(np.float32)

    def runtime(self):
        return {"synthetic": True, "device": "cpu", "dimension": self.dimension}

    def texts(self, texts):
        return normalize(
            np.stack(
                [
                    np.random.default_rng(task_seed(self.cfg["seed"], self.key, text)).normal(
                        size=self.dimension
                    )
                    for text in texts
                ]
            )
        ).astype(np.float32)


def load_encoder(cfg, key):
    return SyntheticEncoder(cfg, key) if cfg["synthetic"] else Encoder(cfg, key)
