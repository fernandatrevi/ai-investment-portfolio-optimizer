"""Download and validate adjusted historical closing prices."""
from datetime import date
import pandas as pd
import yfinance as yf

DEFAULT_TICKERS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "JPM", "JNJ", "XOM"]


def get_prices(tickers: list[str], start: date, end: date) -> pd.DataFrame:
    if not tickers:
        raise ValueError("Select at least one ticker.")
    if start >= end:
        raise ValueError("Start date must be earlier than end date.")
    data = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False, threads=False)
    if data.empty:
        raise ValueError("No historical prices returned. Try another date range.")
    prices = data["Close"]
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])
    prices = prices.reindex(columns=tickers)
    prices = prices.dropna(axis=1, how="all").ffill().dropna()
    if prices.empty or len(prices) < 60:
        raise ValueError("Not enough overlapping trading days (minimum 60).")
    return prices
