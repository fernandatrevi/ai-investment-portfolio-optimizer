# AI Investment Portfolio Optimizer

Educational web dashboard for portfolio analysis with Python, Streamlit and machine learning.

## Features
- Historical adjusted closing prices from Yahoo Finance via yfinance
- Equal-weight vs long-only minimum-variance allocation
- Annualized historical returns, volatility, and correlation heatmaps
- KMeans clustering of assets by historical return and volatility
- Hypothetical USD allocation

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Publish
Deploy this GitHub repository using Streamlit Community Cloud, selecting branch `main` and entrypoint `app.py`. A public app URL is available only after successful deployment.

## Limitations
Educational research only; not investment advice. Optimized weights and reported historical performance use the same sample (in-sample), so this is not a validated forecast. Market data may be missing or delayed. KMeans clustering is descriptive, not predictive. Transaction costs, taxes and slippage are excluded. Walk-forward backtesting is planned.
