import itertools

import numpy as np
import pytest
from scipy.stats import wasserstein_distance

from temporal_drift.metrics.distribution import sliced_wasserstein
from temporal_drift.metrics.retrieval import (
    average_precision_at_k,
    expected_random_ap,
    legacy_ap_at_k,
)
from temporal_drift.metrics.trajectory import angle, trajectory


def test_ap_penalizes_missing_relevant_images():
    relevance = np.r_[True, np.zeros(9, dtype=bool), np.ones(20, dtype=bool)]
    assert average_precision_at_k(relevance, 10) == pytest.approx(0.1)
    assert legacy_ap_at_k(relevance, 10) == 1.0
    assert average_precision_at_k(np.zeros(10), 10) == 0


def test_random_baseline_matches_exhaustive_rankings():
    rankings = set(itertools.permutations([True, True, False, False]))
    expected = np.mean([average_precision_at_k(ranking, 3) for ranking in rankings])
    assert expected_random_ap(4, 2, 3) == pytest.approx(expected)


def test_swd_exact_transport_unequal_clouds():
    a, b = np.array([0.0, 2.0, 5.0]), np.array([-1.0, 1.0, 3.0, 7.0])
    assert sliced_wasserstein(a[:, None], b[:, None], order=1) == pytest.approx(
        wasserstein_distance(a, b)
    )
    assert sliced_wasserstein(a[:, None], a[:, None]) == 0
    assert sliced_wasserstein(np.ones((3, 1)), np.ones((5, 1)) * 3) == pytest.approx(2)


def test_trajectory_null_is_reproducible_and_does_not_modify_inputs():
    rng = np.random.default_rng(2)
    pools = [rng.normal(size=(12, 8)) + i for i in range(3)]
    original = pools[0].copy()
    first = trajectory(pools, permutations=20, seed=42)
    second = trajectory(pools, permutations=20, seed=42)
    np.testing.assert_array_equal(first["null_angles"], second["null_angles"])
    np.testing.assert_array_equal(pools[0], original)
    assert angle(np.array([[0, 0], [1, 0], [2, 0]])) == 0
