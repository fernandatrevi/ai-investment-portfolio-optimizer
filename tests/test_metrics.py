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


def test_first_day_loss_counts_toward_max_drawdown():
    """Starting capital is the first high-water mark, not the first closing value."""
    returns = pd.DataFrame({"A": [-0.10, 0.05, 0.02]})
    stats = portfolio_statistics(returns, np.array([1.0]))
    assert np.isclose(stats["max_drawdown"], -0.10)


def test_first_day_gain_then_loss_uses_historical_peak():
    returns = pd.DataFrame({"A": [0.10, -0.20, 0.05]})
    stats = portfolio_statistics(returns, np.array([1.0]))
    assert np.isclose(stats["max_drawdown"], -0.20)
