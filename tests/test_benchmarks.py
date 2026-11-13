import numpy as np
import pandas as pd
from src.benchmarks import equal_weight_returns, buy_and_hold_curve


def test_equal_weight_returns():
    r = pd.DataFrame({"A": [0.10], "B": [0.00]})
    assert np.isclose(equal_weight_returns(r).iloc[0], 0.05)


def test_buy_and_hold_initial_weights():
    r = pd.DataFrame({"A": [0.10, 0.00], "B": [0.00, 0.10]})
    curve = buy_and_hold_curve(r, np.array([0.5, 0.5]))
    # Each initial $0.50 position grows to $0.55: total $1.10.
    assert np.isclose(curve.iloc[-1], 1.10)


def test_buy_and_hold_does_not_rebalance_after_a_price_change():
    # The asset that grows on day one gets a higher weight on day two.
    # Starting with $0.50 in each asset: A grows to $0.60 then $0.66,
    # while B stays at $0.50. Final wealth is $1.16.
    r = pd.DataFrame({"A": [0.20, 0.10], "B": [0.00, 0.00]})
    curve = buy_and_hold_curve(r, np.array([0.5, 0.5]))
    assert np.allclose(curve.to_numpy(), [1.10, 1.16])
    # Daily equal-weight rebalancing would instead yield $1.155.
    rebalanced = (1 + equal_weight_returns(r)).cumprod()
    assert np.isclose(rebalanced.iloc[-1], 1.155)
    assert not np.isclose(curve.iloc[-1], rebalanced.iloc[-1])
