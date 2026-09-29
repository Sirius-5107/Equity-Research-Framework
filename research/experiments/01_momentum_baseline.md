# Experiment 01 — NIFTY 500 12-Month Momentum Baseline

## Status

**Specification frozen; historical run pending point-in-time constituent data.**

## Hypothesis

A cross-sectional portfolio of NIFTY 500 constituents ranked by trailing 252-trading-day price momentum is evaluated using monthly rebalancing, with the top 20 names held at equal weight.

This experiment is deliberately a one-factor baseline. It is intended to validate the dated research pipeline before introducing composite factor scores.

## Frozen specification

| Item | Specification |
|---|---|
| Universe | NIFTY 500 |
| Constituent method | Point-in-time membership |
| Price | Adjusted close |
| Sample | 2018-01-01 to 2026-08-31 |
| Signal | 252-trading-day trailing return |
| Rebalance | Monthly, last available trading observation |
| Portfolio | Top 20 |
| Weighting | Equal weight |
| Execution | Signal at t, return at t+1 |
| Transaction cost | 5 bps of turnover |
| Risk-free rate | 6% annual |
| Benchmark | NIFTY 500 |

## Why point-in-time membership matters

The repository's ordinary NIFTY 500 loader provides the current constituent list. Projecting that list backward would introduce survivorship bias because securities that entered the index later would be treated as historical constituents while securities that subsequently left would disappear from the historical universe.

The baseline therefore requires dated constituent membership. A public point-in-time NIFTY 500 dataset is documented as an available input, but it is not bundled into this repository.

## Required outputs

The completed run should produce:

- daily net strategy returns;
- target-weight history;
- cumulative equity curve;
- CAGR;
- annualized volatility;
- Sharpe ratio;
- maximum drawdown;
- turnover;
- transaction costs;
- benchmark return series;
- strategy-vs-benchmark comparison;
- subperiod results.

No result should be interpreted as evidence of robustness until sensitivity, cost, and out-of-sample checks are completed.

## Planned robustness tests

After the frozen baseline:

1. Top 10 / 20 / 50.
2. Monthly / quarterly rebalance.
3. 0 / 5 / 10 / 25 bps transaction costs.
4. Pre-2020, 2020–2022, and 2023–2026 subperiods.
5. Out-of-sample evaluation using a pre-declared split.

These are stability checks, not parameter optimization targets.
