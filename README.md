# AI Investment Portfolio Optimizer

**Portfolio Research · Python · Streamlit · Plotly · Quantitative Analytics**

[**Source code and dashboard application**](https://github.com/fernandatrevi/ai-investment-portfolio-optimizer) · [Run with Streamlit Community Cloud](https://share.streamlit.io/)

An interactive **educational** dashboard for exploring historical asset allocation, risk and return. It retrieves adjusted market prices through `yfinance` and compares equal-weight and long-only minimum-variance portfolios.

> **Deployment:** A public working deployment URL has not been verified. The application code is available in this repository but is not automatically hosted by GitHub.

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

## Publish the dashboard

The repository already contains `app.py` and `requirements.txt`. Deploy through [Streamlit Community Cloud](https://share.streamlit.io/), selecting the `main` branch and `app.py` as the entry point. Confirm that the initial data retrieval, charts, exports and holdout tab work in the deployment before adding a live website link here or in GitHub's **About** field.

## Limitations

**Educational research, not financial advice.** Portfolio optimization and overall historical statistics are in-sample. A single historical holdout can still be sensitive to market period, symbol selection and model assumptions. Historical prices may be incomplete or delayed. This dashboard does not account for transaction costs, slippage, tax impact, short sales, investment restrictions or portfolio execution. KMeans clustering is descriptive.

## Skills demonstrated

Python data handling, structured financial analytics, portfolio optimization, scenario interfaces, interactive Plotly visualization, risk reporting, historical holdout evaluation, reproducibility and Git version control.
