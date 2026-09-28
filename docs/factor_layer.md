# Factor Layer

The factor layer converts cleaned market and fundamental data into research
signals. Factor calculations are separated from cross-sectional scoring.

## Factor families

- **Value:** earnings yield, free-cash-flow yield, book-to-market.
- **Quality:** ROE, operating margin, FCF margin, leverage.
- **Growth:** revenue, earnings and FCF growth.
- **Momentum:** trailing total return and cross-sectional momentum.
- **Volatility:** annualized and downside volatility.

The framework does not prescribe a universal factor weighting. Directionality
and weights are explicit inputs to the scoring layer so experiments can compare
specifications without changing factor definitions.

For example, higher earnings yield is generally treated as more favorable in a
value score, while higher leverage or volatility can be treated as less
favorable. These are scoring choices, not properties of the raw measurements.
