import numpy as np
import pandas as pd
from src.optimization import minimum_variance_weights


def test_weights_sum_to_one_and_are_long_only():
    rng = np.random.default_rng(42)
    returns = pd.DataFrame(rng.normal(0, 0.01, (200, 4)), columns=list("ABCD"))
    weights = minimum_variance_weights(returns)
    assert np.isclose(weights.sum(), 1.0)
    assert (weights >= -1e-8).all()
    assert (weights <= 1 + 1e-8).all()


def test_single_asset_gets_full_weight():
    returns = pd.DataFrame({"A": [0.01, -0.02, 0.03]})
    assert minimum_variance_weights(returns).tolist() == [1.0]
