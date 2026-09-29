"""Transaction-cost utilities for portfolio backtests."""
from __future__ import annotations
import numpy as np
import pandas as pd

def turnover(previous_weights: pd.Series, target_weights: pd.Series) -> float:
    weights = pd.concat([previous_weights, target_weights], axis=1).fillna(0.0)
    return float((weights.iloc[:, 1] - weights.iloc[:, 0]).abs().sum())

def transaction_cost(turnover_value: float, cost_rate: float) -> float:
    if not np.isfinite(turnover_value) or turnover_value < 0:
        raise ValueError("turnover must be finite and non-negative")
    if not np.isfinite(cost_rate) or cost_rate < 0:
        raise ValueError("cost_rate must be finite and non-negative")
    return float(turnover_value * cost_rate)
