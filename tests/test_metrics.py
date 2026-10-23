import numpy as np
import pandas as pd
from src.metrics import daily_returns, asset_statistics, portfolio_statistics


def test_constant_prices_have_zero_returns():
    prices = pd.DataFrame({"A": [100.0] * 100, "B": [50.0] * 100})
    returns = daily_returns(prices)
    assert (returns == 0).all().all()
    stats = portfolio_statistics(returns, np.array([0.5, 0.5]))
    assert stats["volatility"] == 0
    assert stats["max_drawdown"] == 0


def test_asset_statistics_preserve_asset_names():
    prices = pd.DataFrame({"A": np.linspace(100, 110, 100), "B": np.linspace(90, 95, 100)})
    assert list(asset_statistics(daily_returns(prices)).index) == ["A", "B"]
