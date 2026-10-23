import numpy as np
import pandas as pd
import pytest
from src.backtest import holdout_backtest


def sample_prices():
    rng = np.random.default_rng(7)
    daily = rng.normal(0.0003, 0.012, (200, 3))
    return pd.DataFrame(100 * np.cumprod(1 + daily, axis=0),
                        index=pd.bdate_range("2024-01-01", periods=200),
                        columns=["A", "B", "C"])


def test_backtest_uses_future_holdout():
    result = holdout_backtest(sample_prices())
    assert result["train_end"] < result["test_start"]
    assert len(result["test_returns"]) > 0
    assert np.isclose(result["weights"].sum(), 1)


def test_backtest_rejects_invalid_fraction():
    with pytest.raises(ValueError):
        holdout_backtest(sample_prices(), 0.3)
