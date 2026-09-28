"""Quality-factor calculations."""
from __future__ import annotations
import pandas as pd

def roe(df: pd.DataFrame) -> pd.Series:
    return df["ROE"].astype(float)

def operating_margin(df: pd.DataFrame) -> pd.Series:
    return df["OperatingMargin"].astype(float)

def fcf_margin(df: pd.DataFrame) -> pd.Series:
    return df["FCFMargin"].astype(float)

def leverage(df: pd.DataFrame) -> pd.Series:
    return df["DebtToEquity"].astype(float)
