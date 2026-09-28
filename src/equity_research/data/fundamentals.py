"""Fundamental-statement access and reusable financial metrics."""

from __future__ import annotations
from collections.abc import Sequence
import numpy as np
import pandas as pd

def get_metric(statement: pd.DataFrame | None, names: Sequence[str]) -> pd.Series | None:
    """Return the first matching statement row, or None."""
    if statement is None or statement.empty:
        return None
    for name in names:
        if name in statement.index:
            return statement.loc[name]
    return None

def revenue(statement): return get_metric(statement, ["Total Revenue", "Operating Revenue"])
def net_income(statement): return get_metric(statement, ["Net Income", "Net Income Common Stockholders"])
def operating_income(statement): return get_metric(statement, ["Operating Income"])
def ebit(statement): return get_metric(statement, ["EBIT"])
def ebitda(statement): return get_metric(statement, ["EBITDA"])
def interest_expense(statement): return get_metric(statement, ["Interest Expense", "Interest Expense Non Operating"])
def total_assets(statement): return get_metric(statement, ["Total Assets"])
def total_debt(statement): return get_metric(statement, ["Total Debt"])
def net_debt(statement): return get_metric(statement, ["Net Debt"])
def equity(statement): return get_metric(statement, ["Stockholders Equity", "Common Stock Equity", "Total Equity Gross Minority Interest"])
def current_assets(statement): return get_metric(statement, ["Current Assets", "Total Current Assets"])
def current_liabilities(statement): return get_metric(statement, ["Current Liabilities", "Total Current Liabilities"])
def operating_cf(statement): return get_metric(statement, ["Operating Cash Flow"])
def free_cf(statement): return get_metric(statement, ["Free Cash Flow"])
def capex(statement): return get_metric(statement, ["Capital Expenditure", "Capital Expenditure Reported"])
def gross_profit(statement): return get_metric(statement, ["Gross Profit"])

def latest_value(series: pd.Series | None) -> float:
    """Return the first finite value, matching Yahoo's newest-first statements."""
    if series is None: return np.nan
    values = pd.to_numeric(series, errors="coerce").dropna()
    return float(values.iloc[0]) if not values.empty else np.nan

def ratio(numerator: float, denominator: float) -> float:
    """Safe ratio; returns NaN for missing or zero denominators."""
    if not np.isfinite(numerator) or not np.isfinite(denominator) or denominator == 0:
        return np.nan
    return numerator / denominator

def debt_equity(bs): return ratio(latest_value(total_debt(bs)), latest_value(equity(bs)))
def current_ratio(bs): return ratio(latest_value(current_assets(bs)), latest_value(current_liabilities(bs)))
def roe(fin, bs): return ratio(latest_value(net_income(fin)), latest_value(equity(bs))) * 100
def roa(fin, bs): return ratio(latest_value(net_income(fin)), latest_value(total_assets(bs))) * 100
def operating_margin(fin): return ratio(latest_value(operating_income(fin)), latest_value(revenue(fin))) * 100
def net_margin(fin): return ratio(latest_value(net_income(fin)), latest_value(revenue(fin))) * 100
def gross_margin(fin): return ratio(latest_value(gross_profit(fin)), latest_value(revenue(fin))) * 100
def interest_coverage(fin): return ratio(latest_value(ebit(fin)), abs(latest_value(interest_expense(fin))))
def fcf_margin(fin, cf): return ratio(latest_value(free_cf(cf)), latest_value(revenue(fin))) * 100
def operating_cf_margin(fin, cf): return ratio(latest_value(operating_cf(cf)), latest_value(revenue(fin))) * 100
def capex_to_revenue(fin, cf): return ratio(abs(latest_value(capex(cf))), latest_value(revenue(fin))) * 100
def net_debt_to_ebitda(fin, bs): return ratio(latest_value(net_debt(bs)), latest_value(ebitda(fin)))

def cagr(series: pd.Series | None, periods_per_year: float = 1.0) -> float:
    """Calculate CAGR from positive observations ordered oldest-to-newest."""
    if series is None: return np.nan
    values = pd.to_numeric(series, errors="coerce").dropna()
    if len(values) < 2 or (values <= 0).any() or periods_per_year <= 0:
        return np.nan
    periods = (len(values) - 1) / periods_per_year
    return (values.iloc[-1] / values.iloc[0]) ** (1 / periods) - 1
