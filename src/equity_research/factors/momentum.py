"""Price-momentum calculations."""
from __future__ import annotations
import numpy as np
import pandas as pd

def total_return(prices: pd.DataFrame, lookback: int) -> pd.DataFrame:
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    return prices / prices.shift(lookback) - 1

def cross_sectional_momentum(prices: pd.DataFrame, lookback: int) -> pd.Series:
    returns = total_return(prices, lookback)
    return returns.iloc[-1].replace([np.inf, -np.inf], np.nan)
