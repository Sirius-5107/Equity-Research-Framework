"""Growth-factor calculations."""
from __future__ import annotations
import pandas as pd

def revenue_growth(df: pd.DataFrame) -> pd.Series:
    return df["RevenueGrowth"].astype(float)

def earnings_growth(df: pd.DataFrame) -> pd.Series:
    return df["EarningsGrowth"].astype(float)

def fcf_growth(df: pd.DataFrame) -> pd.Series:
    return df["FCFGrowth"].astype(float)
