import numpy as np


def average_precision_at_k(relevance, k: int) -> float:
    """AP@k normalized by min(total relevant in the gallery, k)."""
    relevance = np.asarray(relevance, dtype=bool)
    if k < 1:
        raise ValueError("k must be positive")
    denominator = min(int(relevance.sum()), k)
    if denominator == 0:
        return 0.0
    prefix = relevance[:k]
    precision = np.cumsum(prefix) / np.arange(1, len(prefix) + 1)
    return float(np.sum(precision * prefix) / denominator)


def legacy_ap_at_k(relevance, k: int) -> float:
    """Notebook's hit-normalized score, retained only as a labeled diagnostic."""
    prefix = np.asarray(relevance, dtype=bool)[:k]
    if not prefix.any():
        return 0.0
    return float(np.sum(np.cumsum(prefix) / np.arange(1, len(prefix) + 1) * prefix) / prefix.sum())


def expected_random_ap(total: int, relevant: int, k: int) -> float:
    """Exact expected corrected AP@k under a uniformly random ranking."""
    if not 0 <= relevant <= total or k < 1:
        raise ValueError("Invalid gallery counts")
    if relevant == 0:
        return 0.0
    q = min(total, k)
    a = relevant / total
    b = (relevant - 1) / (total - 1) if total > 1 else 0.0
    terms = [(a / rank) * (1 + (rank - 1) * b) for rank in range(1, q + 1)]
    return float(sum(terms) / min(relevant, k))
