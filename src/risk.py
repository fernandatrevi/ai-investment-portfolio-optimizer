"""Additional downside risk measurements."""
import numpy as np
import pandas as pd


def downside_deviation(returns: pd.Series, target_daily: float = 0.0) -> float:
    shortfall = np.minimum(returns.to_numpy(dtype=float) - target_daily, 0.0)
    return float(np.sqrt(np.mean(shortfall ** 2)) * np.sqrt(252))


def historical_var(returns: pd.Series, confidence: float = 0.95) -> float:
    if not 0 < confidence < 1:
        raise ValueError("Confidence must be between zero and one.")
    return float(-returns.quantile(1 - confidence))


def historical_cvar(returns: pd.Series, confidence: float = 0.95) -> float:
    threshold = -historical_var(returns, confidence)
    tail = returns[returns <= threshold]
    return float(-tail.mean()) if len(tail) else 0.0
