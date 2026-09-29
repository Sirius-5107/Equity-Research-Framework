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


## 10. Dated cross-sectional workflow

For cross-sectional factor research, construct signals independently at each rebalance date:

1. Restrict the input data to observations available through date t.
2. Calculate the factor for every eligible security.
3. Rank the cross-section and select the stated top-N portfolio.
4. Persist those target weights until the next rebalance.
5. Let the backtest engine apply the signal at t to returns at t+1.
6. Charge transaction costs from turnover when the target portfolio changes.

The reusable `equity_research.research.cross_sectional` layer implements this workflow. Its `build_target_weight_history` function explicitly prevents future observations from reaching the signal function. The first empirical experiment should use a simple, pre-specified specification such as monthly top-20 12-month momentum before adding additional factors or parameter searches.

A dated cross-sectional backtest is different from a single cross-section helper: the latter is useful for testing the factor/screening plumbing, while the former produces a full time series of historical portfolio instructions.

## 11. Baseline experiment discipline

For the first factor experiment, freeze the specification before looking at results. Record:

- universe and constituent-source date;
- price field and adjustment convention;
- rebalance frequency;
- factor lookback;
- portfolio size;
- weighting scheme;
- transaction-cost assumption;
- benchmark;
- sample period.

Only after the baseline is measured should sensitivity tests vary portfolio size, rebalance frequency, costs, or subperiods. The purpose of these tests is to assess stability rather than search for the highest historical Sharpe.
