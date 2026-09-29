# Factor Layer

The factor layer converts cleaned research inputs into interpretable cross-sectional or time-series measurements.

## Implemented factor families

- Value: earnings yield, free-cash-flow yield, book-to-market
- Quality: ROE, operating margin, FCF margin, leverage
- Growth: revenue growth, earnings growth, FCF growth
- Momentum: total return and cross-sectional momentum
- Volatility: annualized and downside volatility

## Scoring

percentile_score converts a factor into a cross-sectional score in [0, 1].

Direction is explicit:
- higher_is_better=True ranks larger values higher.
- higher_is_better=False ranks smaller values higher.

Composite scores use normalized non-negative weights.

Factor calculations do not prescribe universal weights. Each research experiment must specify and record its weighting scheme.

## Pipeline integration

Factors → Percentile Scores → Composite Score → Top-N Screen → Portfolio Weights → Backtest

## Research caution

Factor scores are descriptive transformations of supplied data. They do not by themselves establish predictive power. Predictive claims require dated, leakage-controlled testing and appropriate robustness analysis.
