import numpy as np
import pandas as pd
from src.risk import downside_deviation, historical_var, historical_cvar


def test_downside_deviation_zero_for_positive_returns():
    assert downside_deviation(pd.Series([0.01, 0.02])) == 0


def test_expected_tail_loss_is_at_least_var():
    returns = pd.Series(np.linspace(-0.10, 0.10, 101))
    assert historical_cvar(returns) >= historical_var(returns)
