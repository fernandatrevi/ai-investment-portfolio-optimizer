# AI Investment Portfolio Optimizer

**Portfolio Research · Python · Streamlit · Plotly · Quantitative Analytics**

[**Source code and dashboard application**](https://github.com/fernandatrevi/ai-investment-portfolio-optimizer) · [Run with Streamlit Community Cloud](https://share.streamlit.io/)

An interactive **educational** dashboard for exploring historical asset allocation, risk and return. It retrieves adjusted market prices through `yfinance` and compares equal-weight and long-only minimum-variance portfolios.

> **Deployment status:** The application is ready to submit to Streamlit Community Cloud; a public URL has not yet been created or verified. Deployment requires signing into the hosting service and selecting this repository.

## Interactive features

| Section | What users can explore |
|---|---|
| Portfolio builder | Choose from preset stock symbols, historical dates and hypothetical USD capital |
| Performance | Interactive adjusted-price and portfolio growth charts |
| Allocation | Equal-weight vs minimum-variance portfolios, USD amounts, weight chart and donut chart |
| Risk | Historical annualized volatility, maximum drawdown, downside deviation, daily VaR and CVaR |
| Asset relationships | Return correlations and descriptive KMeans clustering |
| Holdout evaluation | Change the chronological training fraction (50–90%) and compare subsequent test-period outcomes |
| Exports | Download allocation, risk indicators and holdout comparison as CSV |

All dashboard labels are in English.

## Important methodology

- Market data are historical adjusted prices retrieved by `yfinance`.
- Minimum-variance weights minimize the **estimated in-sample variance**, subject to nonnegative weights that sum to one.
- The equal-weight portfolio is a reference strategy, not an assertion of optimality.
- The plotted strategy paths use **daily constant-weight rebalancing as a simplified illustration**. Real trading costs, taxes and constraints are excluded.
- Daily empirical VaR and CVaR are historical estimates, not guaranteed future losses or upper bounds.
- The holdout evaluation fits on earlier observations and assesses performance on later observations. It is a single chronological split, **not a validated live trading strategy or full walk-forward backtest**.
- KMeans detects descriptive groups in historical return and volatility, not predictions or AI-generated investment advice.

## Launch the app locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Publish the dashboard (Streamlit Community Cloud)

The repository already contains the application entry point (`app.py`), Python dependencies (`requirements.txt`), and the `.streamlit/config.toml` appearance configuration.

1. Open **[Streamlit Community Cloud](https://share.streamlit.io/)** and sign in with the GitHub account `fernandatrevi`.
2. Choose **Create app → Yup, I have an app**.
3. Select **Repository:** `fernandatrevi/ai-investment-portfolio-optimizer`.
4. Select **Branch:** `main` and **Main file path:** `app.py`.
5. Where available, choose **Python 3.12** and optionally set a memorable subdomain.
6. Click **Deploy**, then open the resulting `https://…streamlit.app/` link.
7. Check that market prices load, the Performance/Allocation/Risk/Holdout tabs render, and CSV exports work. If Yahoo Finance rate limits requests, retry later and check Cloud logs.
8. Only **after the public link works**, replace this deployment status note and add the verified URL to the GitHub profile README.

**Do not put passwords, API tokens or credentials in GitHub.** This app uses public Yahoo Finance data, so no secrets are required for this initial deployment. Hosting availability and external market-data access are not guaranteed.


## Limitations

**Educational research, not financial advice.** Portfolio optimization and overall historical statistics are in-sample. A single historical holdout can still be sensitive to market period, symbol selection and model assumptions. Historical prices may be incomplete or delayed. This dashboard does not account for transaction costs, slippage, tax impact, short sales, investment restrictions or portfolio execution. KMeans clustering is descriptive.

## Skills demonstrated

Python data handling, structured financial analytics, portfolio optimization, scenario interfaces, interactive Plotly visualization, risk reporting, historical holdout evaluation, reproducibility and Git version control.
