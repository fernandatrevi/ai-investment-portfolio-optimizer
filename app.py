"""Public interactive investment portfolio research dashboard."""
from datetime import date
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from src.data import DEFAULT_TICKERS, get_prices
from src.metrics import daily_returns, asset_statistics, portfolio_statistics
from src.optimization import minimum_variance_weights
from src.clustering import cluster_assets
from src.backtest import holdout_backtest

st.set_page_config(page_title="AI Investment Portfolio Optimizer", page_icon="📈", layout="wide")
st.title("📈 AI Investment Portfolio Optimizer")
st.caption("Educational research tool · Historical results are not forecasts or investment advice")
with st.sidebar:
    st.header("Portfolio settings")
    tickers = st.multiselect("Select stocks", DEFAULT_TICKERS, default=DEFAULT_TICKERS[:5])
    start = st.date_input("Start date", value=date(2021, 1, 1))
    end = st.date_input("End date (exclusive)", value=date.today())
    capital = st.number_input("Hypothetical capital (USD)", min_value=100.0, value=10000.0, step=1000.0)
if not tickers:
    st.info("Select at least one stock to begin.")
    st.stop()
try:
    with st.spinner("Downloading historical market data..."):
        prices = get_prices(tickers, start, end)
    returns = daily_returns(prices)
    equal_weights = np.repeat(1 / len(prices.columns), len(prices.columns))
    optimized_weights = minimum_variance_weights(returns)
    equal_stats = portfolio_statistics(returns, equal_weights)
    optimized_stats = portfolio_statistics(returns, optimized_weights)
except Exception as exc:
    st.error(f"Could not calculate the portfolio: {exc}")
    st.stop()
st.subheader("Historical price performance")
st.plotly_chart(px.line(prices / prices.iloc[0] * 100, labels={"value": "Indexed price (100 = start)", "index": "Date", "variable": "Stock"}), use_container_width=True)
st.subheader("Portfolio comparison")
c1, c2, c3 = st.columns(3)
c1.metric("Equal weight annualized return", f"{equal_stats['annual_return']:.1%}")
c2.metric("Minimum variance annualized return", f"{optimized_stats['annual_return']:.1%}")
c3.metric("Minimum variance annualized volatility", f"{optimized_stats['volatility']:.1%}")
st.caption("Weights are estimated from the selected historical period; these in-sample figures are not out-of-sample performance.")
allocations = pd.DataFrame({"Stock": prices.columns, "Equal weight": equal_weights, "Minimum variance": optimized_weights})
left, right = st.columns(2)
with left:
    st.plotly_chart(px.bar(allocations.melt(id_vars="Stock", var_name="Method", value_name="Weight"), x="Stock", y="Weight", color="Method", barmode="group", title="Portfolio weights"), use_container_width=True)
with right:
    st.plotly_chart(px.imshow(returns.corr(), text_auto=".2f", aspect="auto", title="Daily return correlations"), use_container_width=True)
st.subheader("Machine learning: asset groups")
clusters = cluster_assets(returns)
st.plotly_chart(px.scatter(clusters.reset_index(names="Stock"), x="Annualized volatility", y="Annualized return", color="Cluster", hover_name="Stock", title="KMeans groups based on historical return and volatility"), use_container_width=True)
st.subheader("Hypothetical capital allocation")
allocations["Optimized USD"] = allocations["Minimum variance"] * capital
st.dataframe(allocations.style.format({"Equal weight": "{:.1%}", "Minimum variance": "{:.1%}", "Optimized USD": "${:,.2f}"}), use_container_width=True, hide_index=True)
st.caption("Important: The clustering is descriptive, not a return prediction. No transaction costs, taxes or slippage are included.")


st.subheader("Out-of-sample historical evaluation")
st.caption("Weights are estimated using the earliest 70% of observations and evaluated on the later 30%. This avoids fitting weights on the test period.")
try:
    evaluation = holdout_backtest(prices)
    st.write(f"Training ends: {evaluation['train_end']} · Test begins: {evaluation['test_start']} · Test ends: {evaluation['test_end']}")
    test_table = pd.DataFrame({
        "Strategy": ["Equal weight", "Minimum variance"],
        "Annualized test return": [evaluation["equal"]["annual_return"], evaluation["optimized"]["annual_return"]],
        "Annualized test volatility": [evaluation["equal"]["volatility"], evaluation["optimized"]["volatility"]],
        "Maximum test drawdown": [evaluation["equal"]["max_drawdown"], evaluation["optimized"]["max_drawdown"]],
    })
    st.dataframe(test_table.style.format({
        "Annualized test return": "{:.2%}",
        "Annualized test volatility": "{:.2%}",
        "Maximum test drawdown": "{:.2%}",
    }), hide_index=True, use_container_width=True)
    test = evaluation["test_returns"]
    eq_growth = (1 + test @ np.repeat(1 / len(test.columns), len(test.columns))).cumprod()
    opt_growth = (1 + test @ evaluation["weights"]).cumprod()
    curves = pd.DataFrame({"Equal weight": eq_growth, "Minimum variance": opt_growth})
    st.plotly_chart(px.line(curves, title="Growth of $1 during the unseen test period", labels={"value": "Portfolio value (USD)", "index": "Date", "variable": "Strategy"}), use_container_width=True)
except ValueError as exc:
    st.warning(f"Not enough data for holdout evaluation: {exc}")
