"""Summaries of the completeness of price histories."""
import pandas as pd


def missing_price_summary(prices: pd.DataFrame) -> pd.DataFrame:
    if prices.empty:
        return pd.DataFrame(columns=["Missing observations", "Missing share"])
    return pd.DataFrame({
        "Missing observations": prices.isna().sum(),
        "Missing share": prices.isna().mean(),
    })


def coverage_dates(prices: pd.DataFrame) -> dict:
    if prices.empty:
        raise ValueError("No price observations.")
    return {"first_date": str(prices.index.min().date()),
            "last_date": str(prices.index.max().date()),
            "trading_days": len(prices)}
