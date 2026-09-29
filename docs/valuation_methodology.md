# Valuation Methodology

The valuation layer contains reusable mechanics for intrinsic and relative
valuation. It does not prescribe a target price or investment conclusion.

## DCF

The DCF flow is:

1. Forecast free cash flow.
2. Discount forecast cash flows using WACC.
3. Estimate terminal value using either:
   - Gordon growth: FCF_(n+1) / (WACC - g)
   - Exit multiple: terminal metric × terminal multiple.
4. Discount terminal value.
5. Bridge enterprise value to equity value:
   EV - debt + cash - minority interest - preferred stock.
6. Divide by shares outstanding for implied share price.

The Gordon-growth method requires WACC > terminal growth.

## Multiples

The framework supports peer mean, peer median, and direct metric × multiple
valuation. Peer statistics are descriptive; peer selection and outlier
treatment should be documented separately for each research exercise.

## Sensitivity

Two-way sensitivity tables vary two assumptions through a supplied evaluator.
This keeps the sensitivity engine independent of the valuation model and allows
WACC/growth, multiple/earnings, or other assumption grids to be tested.

Valuation outputs are model results conditional on assumptions, not forecasts
of realized market prices.
