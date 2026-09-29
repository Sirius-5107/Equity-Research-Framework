# Research Process

The framework separates hypothesis formation, implementation, measurement, and interpretation.

## 1. Define the hypothesis

State the economic intuition, factor directions, universe, rebalance frequency, holding period, benchmark, and transaction-cost/slippage assumptions.

Avoid changing the hypothesis after inspecting the final result without recording the change.

## 2. Define the universe and data

Document constituent source and date, survivorship treatment, price adjustment convention, fundamental source, missing-data policy, corporate-action handling, and information-availability lags.

## 3. Build features and factors

Raw measurements live in the data/factor layers. Factor direction and composite weights are supplied explicitly.

Composite score:

composite = sum(weight_i × percentile_score_i)

A factor where lower values are preferred should use higher_is_better=False.

## 4. Screen and construct the portfolio

The screening layer separates eligibility, ranking, and top-N selection. Portfolio construction then converts selected names or scores into target weights.

## 5. Execute without look-ahead

The default backtesting engine applies a target portfolio observed at date t to asset returns at t+1.

Transaction costs are based on:

cost_t = turnover_t × cost_rate

The repository default is 5 bps, but each experiment should state its actual assumption.

## 6. Measure performance

Report total return, CAGR, annualized volatility, Sharpe ratio, maximum drawdown, Sortino ratio, Calmar ratio, turnover, win rate, and profit factor as appropriate.

Always state return frequency, annualization factor, and risk-free-rate assumption.

## 7. Validate the experiment

Inspect benchmark-relative performance, train/test or out-of-sample behavior, parameter sensitivity, transaction-cost sensitivity, subperiod behavior, missing-data/universe effects, turnover, and concentration.

Where appropriate, add walk-forward validation and placebo tests.

## 8. Interpret results

Separate observed historical results, statistical evidence, economic interpretation, and limitations.

Do not describe a strategy as robust or predictive solely because one backtest produced a favorable historical metric.

## 9. Promote reusable code

Move reusable mechanics into src/, keep experiment-specific assumptions and results in research/, add regression tests, and update methodology documentation.
