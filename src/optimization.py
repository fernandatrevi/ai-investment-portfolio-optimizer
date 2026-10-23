"""Long-only, fully invested minimum-variance allocation."""
import numpy as np
import pandas as pd
from scipy.optimize import minimize


def minimum_variance_weights(returns: pd.DataFrame) -> np.ndarray:
    n = returns.shape[1]
    if n == 1:
        return np.array([1.0])
    covariance = returns.cov().to_numpy() * 252
    objective = lambda w: float(w @ covariance @ w)
    result = minimize(objective, np.repeat(1 / n, n), method="SLSQP", bounds=[(0, 1)] * n,
                      constraints=[{"type": "eq", "fun": lambda w: np.sum(w) - 1}],
                      options={"maxiter": 2000, "ftol": 1e-12})
    if not result.success:
        raise RuntimeError(f"Optimization failed: {result.message}")
    return result.x / result.x.sum()
