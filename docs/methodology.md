# Methodology

## Data
Daily adjusted closing prices from Yahoo Finance (via yfinance). Dates are trading days and the requested end date is exclusive. Stocks must have a shared observation window.

## Descriptive statistics
Daily returns are calculated from adjacent adjusted closing prices. Annualized volatility uses sample standard deviation times sqrt(252). Annualized geometric growth is based on cumulative compounded returns.

## Optimization
Long-only, fully invested minimum-variance optimization solves min(wᵀΣw), subject to sum(w)=1 and 0≤w≤1. The covariance estimate is historical, not a guarantee of future risk.

## ML
KMeans groups assets using standardized historical annualized return and volatility. Cluster labels have no ordinal financial meaning. This is unsupervised descriptive analysis, not a buy/sell signal.

## Holdout evaluation
The first 70% of daily returns are training data. Portfolio weights are fitted on training data only and held constant during the last 30% test period. No random shuffle is used. Comparisons exclude costs, taxes, and slippage. This is a single historical holdout, not a robust rolling backtest.

## Limitations
Survivorship bias, data-provider revisions, regime changes, trading costs and market impact can affect results. This educational prototype does not provide personalized financial advice.
