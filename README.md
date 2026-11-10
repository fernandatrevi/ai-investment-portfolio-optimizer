# AI Investment Portfolio Optimizer

**Portfolio analytics · Python · Streamlit · Machine learning**

**[Explore the GitHub repository](https://github.com/fernandatrevi/ai-investment-portfolio-optimizer)**

An educational web dashboard for studying portfolio allocation and historical risk/return characteristics. The project uses Python, Streamlit, historical financial data and machine-learning techniques.

> **Deployment status:** No verified public demo URL is documented for this project. To use the dashboard, run it locally using the instructions below. A live application link can be added after successful deployment.

## Features

- Retrieves historical adjusted closing prices from Yahoo Finance with `yfinance`.
- Compares equal-weight allocations with a long-only minimum-variance allocation.
- Reports annualized historical returns and volatility.
- Visualizes correlations between assets.
- Uses KMeans to group assets by historical return and volatility.
- Calculates hypothetical allocations in USD.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows activate the virtual environment with `.venv\Scripts\activate`.

## Deploy a public demo

Use [Streamlit Community Cloud](https://share.streamlit.io/) to deploy this GitHub repository. Select the `main` branch and `app.py` as the entry point. Add a public demo URL to this README and to the repository's **About → Website** field *only after* a successful deployment has been tested.

## Model limitations

**Educational analysis only — not investment advice.** Optimized portfolio weights and historical performance are evaluated in-sample, so the analysis does not validate future returns. Market data can be delayed, unavailable or incomplete. KMeans clustering is descriptive, not predictive. The analysis excludes transaction costs, taxes and slippage. Walk-forward backtesting remains a proposed improvement.

## Key competencies

Portfolio modeling, data preparation, historical risk metrics, constrained optimization, exploratory clustering and interactive dashboard development.
