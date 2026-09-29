# Backtesting Methodology

The backtesting layer converts dated signals into portfolio returns while making execution timing, turnover, and costs explicit.

## Signal timing

A target weight observed at date t is applied to the asset return at t+1. This one-period lag is the framework default and prevents a signal calculated from information at t from being credited with the same-period return.

## Portfolio construction

The framework supports equal-weight portfolios, positive-score weighted portfolios, and normalization to a 100% long-only portfolio.

## Transaction costs

Turnover is the sum of absolute changes in asset weights between consecutive target portfolios. Transaction cost equals turnover multiplied by the cost rate. The default configuration uses 5 bps, but the engine accepts an explicit rate.

## Performance metrics

The layer provides total return, CAGR, annualized volatility, Sharpe ratio, maximum drawdown, downside volatility, Sortino ratio, Calmar ratio, win rate, and profit factor.

## Research safeguards

Backtest results should document universe and survivorship treatment, data availability, signal formation timing, execution convention, transaction costs and slippage, benchmark, in-sample/out-of-sample split, and parameter sensitivity.

The engine does not declare a strategy successful or generalizable. Historical performance is conditional on the supplied data and assumptions.
