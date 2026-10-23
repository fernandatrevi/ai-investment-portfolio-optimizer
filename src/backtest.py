"""Chronological holdout test for portfolio allocations."""
import numpy as np
import pandas as pd
from .metrics import daily_returns, portfolio_statistics
from .optimization import minimum_variance_weights


def holdout_backtest(prices: pd.DataFrame, train_fraction: float = 0.7) -> dict:
    """Fit weights on the earlier period, evaluate on later unseen returns."""
    if not 0.5 <= train_fraction <= 0.9:
        raise ValueError("Training fraction must be between 0.5 and 0.9.")
    returns = daily_returns(prices)
    if len(returns) < 80:
        raise ValueError("At least 80 daily returns are required.")
    cutoff = int(len(returns) * train_fraction)
    train, test = returns.iloc[:cutoff], returns.iloc[cutoff:]
    optimized = minimum_variance_weights(train)
    equal = np.repeat(1 / len(optimized), len(optimized))
    return {
        "train_end": str(train.index[-1].date()),
        "test_start": str(test.index[0].date()),
        "test_end": str(test.index[-1].date()),
        "weights": optimized,
        "equal": portfolio_statistics(test, equal),
        "optimized": portfolio_statistics(test, optimized),
        "test_returns": test,
    }
