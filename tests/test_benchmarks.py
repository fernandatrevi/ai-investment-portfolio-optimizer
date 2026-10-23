import numpy as np
import pandas as pd
from src.benchmarks import equal_weight_returns, buy_and_hold_curve


def test_equal_weight_returns():
    r = pd.DataFrame({"A": [0.10], "B": [0.00]})
    assert np.isclose(equal_weight_returns(r).iloc[0], 0.05)


def test_buy_and_hold_initial_weights():
    r = pd.DataFrame({"A": [0.10, 0.00], "B": [0.00, 0.10]})
    curve = buy_and_hold_curve(r, np.array([0.5, 0.5]))
    assert np.isclose(curve.iloc[-1], 1.105)
