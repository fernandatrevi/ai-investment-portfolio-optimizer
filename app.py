"""Interactive educational portfolio-analysis dashboard.

The optimization is in-sample; the chronological holdout is a separate evaluation.
Not financial advice or a prediction of investment performance.
"""
from datetime import date, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.backtest import holdout_backtest
from src.clustering import cluster_assets
from src.data import DEFAULT_TICKERS, get_prices
from src.metrics import daily_returns, portfolio_statistics
from src.optimization import minimum_variance_weights
from src.risk import downside_deviation, historical_var, historical_cvar

st.set_page_config(
    page_title="AI Investment Portfolio Optimizer",
    page_icon="📈",
    layout="wide",
)

st.title("📈 AI Investment Portfolio Optimizer")
st.caption(
    "Interactive portfolio research · Historic results are not forecasts or investment advice"
)

with st.sidebar:
    st.header("Portfolio builder")
    tickers = st.multiselect(
        "Assets",
        DEFAULT_TICKERS,
        default=DEFAULT_TICKERS[:5],
        help="The available universe is a predefined selection, not the entire stock market.",
    )
    start = st.date_input("Start date", value=date(2021, 1, 1))
    end = st.date_input("End date (exclusive)", value=date.today())
    capital = st.number_input(
        "Hypothetical investment (USD)",
        min_value=100.0,
        value=10000.0,
        step=500.0,
    )
    st.divider()
    st.subheader("Risk and evaluation")
    confidence = st.select_slider(
        "Historical VaR / CVaR confidence",
        options=[0.90, 0.95, 0.99],
        value=0.95,
        format_func=lambda value: f"{value:.0%}",
    )
    training_fraction = st.slider(
        "Holdout training share",
        min_value=0.50,
        max_value=0.90,
        value=0.70,
        step=0.05,
        help="Weights are fitted on the earlier period and tested on later observations.",
    )
    show_prices = st.checkbox("Show normalized asset prices", value=True)
    st.caption("Data source: Yahoo Finance via yfinance. Availability may vary.")

if not tickers:
    st.info("Choose at least one asset in the sidebar.")
    st.stop()
if start >= end:
    st.error("The start date must be earlier than the end date.")
    st.stop()

@st.cache_data(ttl=3600, show_spinner=False)
def load_prices(symbols, start_date, end_date):
    return get_prices(list(symbols), start_date, end_date)

try:
    with st.spinner("Retrieving historical prices and calculating portfolios..."):
        prices = load_prices(tuple(tickers), start, end)
        returns = daily_returns(prices)
        if returns.empty:
            raise ValueError("No valid daily returns were available.")
        assets = list(prices.columns)
        equal_weights = np.repeat(1.0 / len(assets), len(assets))
        optimized_weights = minimum_variance_weights(returns)
        equal_stats = portfolio_statistics(returns, equal_weights)
        optimized_stats = portfolio_statistics(returns, optimized_weights)
except (ValueError, KeyError, RuntimeError) as exc:
    st.error(f"Unable to build the portfolio: {exc}")
    st.stop()
except Exception as exc:
    st.error("The price service or analysis failed. Check the symbols and dates and retry.")
    st.exception(exc)
    st.stop()

if len(assets) != len(tickers):
    missing = sorted(set(tickers) - set(assets))
    st.warning(
        "Data were unavailable for some selected symbols: "
        + ", ".join(missing)
        + ". Analysis uses only assets with usable prices."
    )

asset_returns = returns
eq_daily = asset_returns @ equal_weights
opt_daily = asset_returns @ optimized_weights

def risk_row(label, daily, stats):
    return {
        "Strategy": label,
        "Annualized historical return": stats["annual_return"],
        "Annualized volatility": stats["volatility"],
        "Maximum drawdown": stats["max_drawdown"],
        "Downside deviation": downside_deviation(daily),
        "Historical daily VaR": historical_var(daily, confidence),
        "Historical daily CVaR": historical_cvar(daily, confidence),
    }

risk = pd.DataFrame([
    risk_row("Equal weight", eq_daily, equal_stats),
    risk_row("Minimum variance", opt_daily, optimized_stats),
])
allocations = pd.DataFrame({
    "Asset": assets,
    "Equal weight": equal_weights,
    "Minimum variance": optimized_weights,
})
allocations["Equal-weight USD"] = allocations["Equal weight"] * capital
allocations["Minimum-variance USD"] = allocations["Minimum variance"] * capital

st.subheader("Portfolio overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Assets analyzed", len(assets))
c2.metric("Equal-weight volatility", f"{equal_stats['volatility']:.2%}")
c3.metric("Minimum-variance volatility", f"{optimized_stats['volatility']:.2%}")
c4.metric("Minimum-variance max drawdown", f"{optimized_stats['max_drawdown']:.2%}")
st.caption(
    f"Period: {prices.index.min().date()} to {prices.index.max().date()} · "
    f"{len(returns):,} daily return observations · "
    "The optimizer fits the same historical sample shown in the overview."
)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Performance", "⚖️ Allocation", "🛡️ Risk", "🧪 Holdout evaluation"
])

with tab1:
    if show_prices:
        indexed = prices.div(prices.iloc[0]).mul(100)
        st.plotly_chart(
            px.line(
                indexed,
                labels={"value": "Indexed adjusted price (100 = start)",
                        "index": "Date", "variable": "Asset"},
                title="Historical adjusted-price comparison",
            ),
            use_container_width=True,
        )
    st.caption(
        "Illustrative daily rebalanced portfolio paths; no fees or taxes. "
        "These in-sample weights must not be interpreted as a trading recommendation."
    )
    curves = pd.DataFrame({
        "Equal weight": (1 + eq_daily).cumprod() * capital,
        "Minimum variance": (1 + opt_daily).cumprod() * capital,
    })
    st.plotly_chart(
        px.line(
            curves,
            labels={"value": "Hypothetical portfolio value (USD)",
                    "index": "Date", "variable": "Strategy"},
            title="Historical in-sample portfolio paths",
        ),
        use_container_width=True,
    )
    st.dataframe(
        risk[["Strategy", "Annualized historical return",
              "Annualized volatility", "Maximum drawdown"]].style.format({
            "Annualized historical return": "{:.2%}",
            "Annualized volatility": "{:.2%}",
            "Maximum drawdown": "{:.2%}",
        }),
        use_container_width=True,
        hide_index=True,
    )

with tab2:
    left, right = st.columns([3, 2])
    with left:
        melted = allocations.melt(
            id_vars="Asset", value_vars=["Equal weight", "Minimum variance"],
            var_name="Strategy", value_name="Weight",
        )
        fig = px.bar(
            melted, x="Asset", y="Weight", color="Strategy",
            barmode="group", title="Allocation comparison",
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.plotly_chart(
            px.pie(
                allocations,
                names="Asset", values="Minimum variance",
                title="Minimum-variance allocation",
                hole=0.45,
            ),
            use_container_width=True,
        )
    st.dataframe(
        allocations.style.format({
            "Equal weight": "{:.2%}",
            "Minimum variance": "{:.2%}",
            "Equal-weight USD": "${:,.2f}",
            "Minimum-variance USD": "${:,.2f}",
        }),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download allocation CSV",
        allocations.to_csv(index=False).encode("utf-8"),
        file_name="portfolio_allocations.csv",
        mime="text/csv",
    )
    st.caption("Capital allocation is hypothetical. Share counts and transaction costs are excluded.")

with tab3:
    st.subheader("Historical risk comparison")
    st.dataframe(
        risk.style.format({
            key: "{:.2%}" for key in risk.columns if key != "Strategy"
        }),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(
        f"Daily historical VaR and CVaR shown at {confidence:.0%} confidence. "
        "These backward-looking empirical estimates can underestimate future tail risk."
    )
    lcol, rcol = st.columns(2)
    with lcol:
        corr = returns.corr()
        st.plotly_chart(
            px.imshow(
                corr, text_auto=".2f", zmin=-1, zmax=1,
                color_continuous_scale="RdBu", title="Daily return correlations",
            ),
            use_container_width=True,
        )
    with rcol:
        try:
            if len(assets) >= 2:
                grouped = cluster_assets(returns).reset_index(names="Asset")
                st.plotly_chart(
                    px.scatter(
                        grouped, x="Annualized volatility", y="Annualized return",
                        color="Cluster", hover_name="Asset",
                        title="KMeans: descriptive asset groups",
                    ),
                    use_container_width=True,
                )
            else:
                st.info("Choose at least two assets to compare clusters.")
        except ValueError as exc:
            st.warning(f"Clustering is unavailable for this selection: {exc}")
    st.download_button(
        "Download risk metrics CSV",
        risk.to_csv(index=False).encode("utf-8"),
        file_name="portfolio_risk_metrics.csv",
        mime="text/csv",
    )
    st.caption("KMeans groups historical patterns; it does not predict stock prices.")

with tab4:
    st.subheader("Chronological train/test evaluation")
    st.write(
        "Weights are fitted using the earliest part of the observations. "
        "Performance is then evaluated on the later, unseen historical period. "
        "This is one holdout split, **not** a complete walk-forward backtest."
    )
    try:
        evaluation = holdout_backtest(prices, train_fraction=training_fraction)
        st.caption(
            f"Training ends: {evaluation['train_end']} · "
            f"Test starts: {evaluation['test_start']} · "
            f"Test ends: {evaluation['test_end']}"
        )
        test_table = pd.DataFrame({
            "Strategy": ["Equal weight", "Minimum variance"],
            "Annualized test return": [
                evaluation["equal"]["annual_return"],
                evaluation["optimized"]["annual_return"],
            ],
            "Annualized test volatility": [
                evaluation["equal"]["volatility"],
                evaluation["optimized"]["volatility"],
            ],
            "Maximum test drawdown": [
                evaluation["equal"]["max_drawdown"],
                evaluation["optimized"]["max_drawdown"],
            ],
        })
        st.dataframe(
            test_table.style.format({
                "Annualized test return": "{:.2%}",
                "Annualized test volatility": "{:.2%}",
                "Maximum test drawdown": "{:.2%}",
            }),
            use_container_width=True, hide_index=True,
        )
        test = evaluation["test_returns"]
        eq_growth = (1 + test @ np.repeat(1 / len(test.columns), len(test.columns))).cumprod()
        opt_growth = (1 + test @ evaluation["weights"]).cumprod()
        test_curves = pd.DataFrame({
            "Equal weight": eq_growth * capital,
            "Minimum variance": opt_growth * capital,
        })
        st.plotly_chart(
            px.line(
                test_curves,
                title="Test-period hypothetical portfolio paths",
                labels={"value": "Hypothetical portfolio value (USD)",
                        "index": "Date", "variable": "Strategy"},
            ),
            use_container_width=True,
        )
        st.download_button(
            "Download holdout comparison CSV",
            test_table.to_csv(index=False).encode("utf-8"),
            file_name="holdout_comparison.csv",
            mime="text/csv",
        )
    except ValueError as exc:
        st.warning(f"Insufficient data for this holdout configuration: {exc}")
    except (RuntimeError, KeyError) as exc:
        st.warning(f"Holdout evaluation could not be calculated: {exc}")

st.divider()
st.caption(
    "Educational research only. Historical optimized allocations can be unstable, "
    "and past performance does not predict future returns. "
    "Costs, taxes, slippage and portfolio rebalancing feasibility are not modeled."
)
