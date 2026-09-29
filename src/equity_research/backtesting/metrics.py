"""Performance metrics for return series."""
from __future__ import annotations
import numpy as np
import pandas as pd

def total_return(returns: pd.Series) -> float:
    values = pd.to_numeric(returns, errors="coerce").dropna()
    return np.nan if values.empty else float((1.0 + values).prod() - 1.0)

def cagr(returns: pd.Series, periods_per_year: float = 252.0) -> float:
    values = pd.to_numeric(returns, errors="coerce").dropna()
    if values.empty or periods_per_year <= 0:
        raise ValueError("returns must be non-empty and periods_per_year must be positive")
    growth = float((1.0 + values).prod())
    years = len(values) / periods_per_year
    return np.nan if growth <= 0 else float(growth ** (1.0 / years) - 1.0)

def annualized_volatility(returns: pd.Series, periods_per_year: float = 252.0) -> float:
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    values = pd.to_numeric(returns, errors="coerce").dropna()
    return float(values.std(ddof=1) * np.sqrt(periods_per_year))

def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0, periods_per_year: float = 252.0) -> float:
    values = pd.to_numeric(returns, errors="coerce").dropna()
    if values.empty or periods_per_year <= 0:
        return np.nan
    periodic_rf = (1.0 + risk_free_rate) ** (1.0 / periods_per_year) - 1.0
    excess = values - periodic_rf
    vol = excess.std(ddof=1)
    return np.nan if vol == 0 or np.isnan(vol) else float(excess.mean() / vol * np.sqrt(periods_per_year))

def max_drawdown(returns: pd.Series) -> float:
    values = pd.to_numeric(returns, errors="coerce").dropna()
    if values.empty:
        return np.nan
    equity = (1.0 + values).cumprod()
    return float((equity / equity.cummax() - 1.0).min())

def downside_volatility(returns: pd.Series, periods_per_year: float = 252.0) -> float:
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    downside = pd.to_numeric(returns, errors="coerce").dropna()
    downside = downside[downside < 0]
    return 0.0 if downside.empty else float(downside.std(ddof=1) * np.sqrt(periods_per_year))

def sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.0, periods_per_year: float = 252.0) -> float:
    downside = downside_volatility(returns, periods_per_year)
    return np.nan if downside == 0 else float((cagr(returns, periods_per_year) - risk_free_rate) / downside)

def calmar_ratio(returns: pd.Series, periods_per_year: float = 252.0) -> float:
    dd = max_drawdown(returns)
    return np.nan if dd == 0 or np.isnan(dd) else float(cagr(returns, periods_per_year) / abs(dd))

def win_rate(returns: pd.Series) -> float:
    values = pd.to_numeric(returns, errors="coerce").dropna()
    return np.nan if values.empty else float((values > 0).mean())

def profit_factor(returns: pd.Series) -> float:
    values = pd.to_numeric(returns, errors="coerce").dropna()
    gains = values[values > 0].sum()
    losses = -values[values < 0].sum()
    if losses == 0:
        return np.inf if gains > 0 else np.nan
    return float(gains / losses)
