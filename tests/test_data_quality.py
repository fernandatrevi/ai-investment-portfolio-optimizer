import pandas as pd
from src.data_quality import missing_price_summary, coverage_dates


def test_missing_prices_are_counted():
    prices = pd.DataFrame({"A": [1.0, None], "B": [1.0, 2.0]})
    summary = missing_price_summary(prices)
    assert summary.loc["A", "Missing observations"] == 1
    assert summary.loc["B", "Missing share"] == 0


def test_coverage_counts_rows():
    prices = pd.DataFrame({"A": [1, 2]}, index=pd.date_range("2024-01-01", periods=2))
    assert coverage_dates(prices)["trading_days"] == 2
