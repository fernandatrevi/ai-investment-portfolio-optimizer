"""Input checks for portfolio calculations."""
import numpy as np
import pandas as pd


def validate_returns(returns: pd.DataFrame) -> None:
    if returns.empty:
        raise ValueError("No returns available.")
    if not np.isfinite(returns.to_numpy()).all():
        raise ValueError("Returns contain non-finite values.")
    if (returns <= -1).any().any():
        raise ValueError("Returns contain an invalid loss of 100% or more.")
