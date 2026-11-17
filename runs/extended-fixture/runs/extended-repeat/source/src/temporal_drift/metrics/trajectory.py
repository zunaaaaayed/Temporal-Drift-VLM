import numpy as np

from .distribution import centroid


def angle(centroids) -> float:
    a, b, c = centroids
    u, v = b - a, c - b
    norm = np.linalg.norm(u) * np.linalg.norm(v)
    if norm < 1e-15:
        return float("nan")
    return float(np.degrees(np.arccos(np.clip(np.dot(u, v) / norm, -1, 1))))


def trajectory(pools, *, permutations: int, seed: int) -> dict:
    if any(len(p) < 2 for p in pools):
        raise ValueError("Each trajectory bin needs at least two embeddings")
    observed = angle([centroid(p) for p in pools])
    data = np.vstack(pools)
    cuts = np.cumsum([len(p) for p in pools])[:-1]
    rng = np.random.default_rng(seed)
    null = np.array(
        [
            angle([centroid(group) for group in np.split(data[rng.permutation(len(data))], cuts)])
            for _ in range(permutations)
        ]
    )
    null = null[np.isfinite(null)]
    median = float(np.median(null)) if len(null) else float("nan")
    return {
        "theta_vis": observed,
        "null_median": median,
        "delta_theta": median - observed,
        "permutation_p": float((1 + np.sum(null <= observed)) / (1 + len(null))),
        "null_angles": null,
    }
