"""Execution and signal-alignment utilities."""
from __future__ import annotations
import pandas as pd

def next_period_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """Align a return matrix so a signal at t is applied to return at t+1."""
    return returns.shift(-1)

def apply_transaction_cost(gross_returns: pd.Series, turnover_series: pd.Series, cost_rate: float) -> pd.Series:
    costs = turnover_series.reindex(gross_returns.index).fillna(0.0) * cost_rate
    return gross_returns - costs
