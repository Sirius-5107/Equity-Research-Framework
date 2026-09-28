"""Value-factor calculations."""
from __future__ import annotations
import numpy as np
import pandas as pd

def earnings_yield(df: pd.DataFrame) -> pd.Series:
    return _safe_divide(df["Earnings"], df["MarketCap"])

def fcf_yield(df: pd.DataFrame) -> pd.Series:
    return _safe_divide(df["FreeCashFlow"], df["MarketCap"])

def book_to_market(df: pd.DataFrame) -> pd.Series:
    return _safe_divide(df["BookValue"], df["MarketCap"])

def _safe_divide(a: pd.Series, b: pd.Series) -> pd.Series:
    result = a.astype(float).div(b.astype(float))
    return result.replace([np.inf, -np.inf], np.nan)
