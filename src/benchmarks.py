"""Simple reference strategies used to evaluate optimizers."""
import numpy as np
import pandas as pd


def equal_weight_returns(returns: pd.DataFrame) -> pd.Series:
    if returns.shape[1] == 0:
        raise ValueError("No assets supplied.")
    weights = np.repeat(1.0 / returns.shape[1], returns.shape[1])
    return returns @ weights


def buy_and_hold_curve(returns: pd.DataFrame, weights: np.ndarray) -> pd.Series:
    """Fixed initial shares, no rebalancing, normalized to one dollar."""
    if len(weights) != returns.shape[1]:
        raise ValueError("Weights do not match the number of assets.")
    asset_growth = (1 + returns).cumprod()
    return asset_growth @ weights
