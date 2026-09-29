# Equity Research & Quantitative Screening Framework

A research-oriented Python framework for quantitative equity research: universe/data handling, fundamentals, factor construction, screening, valuation, portfolio backtesting, diagnostics, and reporting.

## Architecture

Universe / Market Data
→ Fundamentals / Feature Engineering
→ Factors
→ Cross-sectional Scoring
→ Screening / Portfolio Construction
→ Lagged Execution + Transaction Costs
→ Backtest Metrics
→ Diagnostics / Research Reports

## Current implementation

- **Data:** NIFTY 500 universe normalization, Yahoo Finance OHLCV download, cleaning, and fundamental metric helpers.
- **Factors:** value, quality, growth, momentum, volatility, percentile scoring, and weighted composite scores.
- **Screening:** eligibility filters, ranking, and configurable top-N selection.
- **Valuation:** DCF, terminal values, peer multiples, and two-way sensitivity analysis.
- **Backtesting:** portfolio construction, one-period signal lag, turnover, transaction costs, and performance metrics.
- **Research runner:** dated cross-sectional signals, monthly rebalance dates, persistent target weights, and point-in-time signal generation can feed the existing lagged backtest engine.
- **Integration:** factor scores can feed screening and target portfolio weights, which can then be passed into the backtesting engine.

## Research principles

1. Signals are separated from portfolio construction.
2. A signal observed at time t is applied to the return at t+1 by default.
3. Transaction costs are charged from portfolio turnover.
4. Factor direction and weights are explicit.
5. Historical backtest performance is conditional evidence, not proof of future performance.
6. Research should include benchmark, out-of-sample, sensitivity, and robustness analysis before conclusions are promoted.

## Repository structure

- src/equity_research/data/ — universe, market data, fundamentals, cleaning
- src/equity_research/factors/ — factor definitions and scoring
- src/equity_research/screening/ — filters, ranking, screening
- src/equity_research/valuation/ — DCF, multiples, sensitivity
- src/equity_research/backtesting/ — execution, portfolios, costs, metrics
- src/equity_research/research_pipeline.py — factor-to-screen-to-backtest integration
- src/equity_research/research/ — dated cross-sectional research workflows
- tests/ — unit tests
- docs/ — methodology and data documentation
- research/ — experiment-specific artifacts
- notebooks/ — exploratory analysis

## Status

Core research infrastructure now includes a reusable dated cross-sectional runner in addition to the factor → screening → valuation/backtesting stages. The next stage is to run a fully specified NIFTY 500 experiment with an explicit benchmark, out-of-sample period, and robustness tests.
