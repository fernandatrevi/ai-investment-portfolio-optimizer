# How to interpret the dashboard

**Annualized return:** compounded historical daily returns, scaled to a 252-trading-day year. It is not a forecast.

**Volatility:** standard deviation of daily returns times the square root of 252. This does not fully capture tail risk.

**Maximum drawdown:** the largest peak-to-trough decline over the selected observed period.

**Correlation:** historical co-movement of daily returns. Correlations may change during market stress.

**Minimum-variance allocation:** portfolio weights chosen to minimize estimated historical covariance risk subject to no short selling and full investment.

**KMeans clusters:** groups of stocks with similar standardized historical return and volatility. Cluster numbers are arbitrary, not rankings.

**Out-of-sample test:** weights learned before the holdout interval and evaluated later. A single holdout is still not sufficient to establish investment skill.

**Historical VaR and CVaR:** empirical loss quantile and mean loss beyond the tail threshold. These can underestimate extreme future losses.
