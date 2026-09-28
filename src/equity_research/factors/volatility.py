"""Risk and volatility calculations."""
from __future__ import annotations
import numpy as np
import pandas as pd

def annualized_volatility(returns: pd.DataFrame, periods_per_year: int = 252) -> pd.Series:
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    return returns.std(ddof=1) * np.sqrt(periods_per_year)

def downside_volatility(returns: pd.DataFrame, periods_per_year: int = 252) -> pd.Series:
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    downside = returns.where(returns < 0)
    return downside.std(ddof=1) * np.sqrt(periods_per_year)
