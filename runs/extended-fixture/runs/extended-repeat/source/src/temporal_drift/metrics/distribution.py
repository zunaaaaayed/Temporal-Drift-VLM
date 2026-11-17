from __future__ import annotations

import numpy as np


def normalize(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    if not np.isfinite(x).all():
        raise ValueError("Non-finite embeddings")
    lengths = np.linalg.norm(x, axis=-1, keepdims=True)
    if np.any(lengths < 1e-15):
        raise ValueError("Zero-length embedding")
    return x / lengths


def centroid(x: np.ndarray) -> np.ndarray:
    return normalize(np.mean(x, axis=0))


def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(1 - np.clip(np.dot(normalize(a), normalize(b)), -1, 1))


def sliced_wasserstein(x, y, *, projections=200, order=2, seed=42) -> float:
    """Exact empirical 1D transport, averaged over seeded unit projections.

    For p=2 return sqrt(mean(W2**2)); for p=1 return mean(W1).
    Unequal sample sizes use the exact piecewise-constant quantile integral.
    Notebook POT calls implicitly selected p=2 despite its W1 markdown.
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.ndim != 2 or y.ndim != 2 or x.shape[1] != y.shape[1]:
        raise ValueError("Expected two embedding matrices with equal dimensions")
    if len(x) < 2 or len(y) < 2:
        return float("nan")
    if order not in (1, 2) or projections < 1:
        raise ValueError("Invalid SWD settings")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("Non-finite embeddings")
    directions = np.random.RandomState(seed).normal(size=(x.shape[1], projections))
    directions /= np.linalg.norm(directions, axis=0, keepdims=True)
    sx, sy = np.sort(x @ directions, axis=0), np.sort(y @ directions, axis=0)
    boundaries = np.unique(np.r_[np.arange(len(x) + 1) / len(x), np.arange(len(y) + 1) / len(y)])
    midpoints = (boundaries[:-1] + boundaries[1:]) / 2
    ix = np.minimum((midpoints * len(x)).astype(int), len(x) - 1)
    iy = np.minimum((midpoints * len(y)).astype(int), len(y) - 1)
    cost = np.abs(sx[ix] - sy[iy]) ** order
    value = np.mean(np.sum(cost * np.diff(boundaries)[:, None], axis=0))
    return float(value ** (1 / order))


def top_k(pool, query, k):
    # Stable order resolves ties by the globally sorted image ID order.
    return pool[np.argsort(-(pool @ query), kind="stable")[:k]]
