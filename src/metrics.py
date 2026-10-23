"""Risk and return statistics from daily prices."""
import numpy as np
import pandas as pd

TRADING_DAYS = 252


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()


def asset_statistics(returns: pd.DataFrame) -> pd.DataFrame:
    annual_return = (1 + returns).prod() ** (TRADING_DAYS / len(returns)) - 1
    volatility = returns.std() * np.sqrt(TRADING_DAYS)
    return pd.DataFrame({"Annualized return": annual_return, "Annualized volatility": volatility})


def portfolio_statistics(returns: pd.DataFrame, weights: np.ndarray) -> dict:
    weighted = returns @ weights
    growth = (1 + weighted).cumprod()
    annual_return = float(growth.iloc[-1] ** (TRADING_DAYS / len(weighted)) - 1)
    volatility = float(weighted.std() * np.sqrt(TRADING_DAYS))
    drawdown = float((growth / growth.cummax() - 1).min())
    return {"annual_return": annual_return, "volatility": volatility, "max_drawdown": drawdown}
