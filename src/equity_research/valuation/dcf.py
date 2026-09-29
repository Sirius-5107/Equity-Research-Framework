"""Discounted cash-flow valuation utilities."""
from __future__ import annotations
import numpy as np
import pandas as pd

def discount_factors(periods: int, wacc: float) -> pd.Series:
    if periods <= 0:
        raise ValueError("periods must be positive")
    if wacc <= -1:
        raise ValueError("wacc must be greater than -100%")
    return pd.Series([(1 + wacc) ** -t for t in range(1, periods + 1)])

def present_value(cash_flows: pd.Series, wacc: float) -> float:
    if cash_flows.empty:
        raise ValueError("cash_flows cannot be empty")
    if wacc <= -1:
        raise ValueError("wacc must be greater than -100%")
    periods = np.arange(1, len(cash_flows) + 1)
    values = pd.to_numeric(cash_flows, errors="coerce").to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("cash_flows must contain only finite values")
    return float(np.sum(values / (1 + wacc) ** periods))

def terminal_value_gordon(final_fcf: float, growth: float, wacc: float) -> float:
    if not np.isfinite(final_fcf) or not np.isfinite(growth) or not np.isfinite(wacc):
        raise ValueError("inputs must be finite")
    if wacc <= growth:
        raise ValueError("wacc must be greater than terminal growth")
    return final_fcf * (1 + growth) / (wacc - growth)

def terminal_value_exit_multiple(metric: float, multiple: float) -> float:
    if not np.isfinite(metric) or not np.isfinite(multiple):
        raise ValueError("inputs must be finite")
    if multiple < 0:
        raise ValueError("multiple must be non-negative")
    return metric * multiple

def enterprise_value(
    forecast_fcf: pd.Series,
    wacc: float,
    terminal_value: float,
) -> float:
    return present_value(forecast_fcf, wacc) + terminal_value / (1 + wacc) ** len(forecast_fcf)

def equity_value(
    enterprise_value_value: float,
    debt: float,
    cash: float,
    minority_interest: float = 0.0,
    preferred_stock: float = 0.0,
) -> float:
    return enterprise_value_value - debt + cash - minority_interest - preferred_stock

def implied_share_price(equity_value_value: float, shares_outstanding: float) -> float:
    if shares_outstanding <= 0:
        raise ValueError("shares_outstanding must be positive")
    return equity_value_value / shares_outstanding
