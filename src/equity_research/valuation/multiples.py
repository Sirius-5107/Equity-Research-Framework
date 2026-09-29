"""Comparable-company and trading-multiple utilities."""
from __future__ import annotations
import numpy as np
import pandas as pd

def implied_value(metric: float, multiple: float) -> float:
    if not np.isfinite(metric) or not np.isfinite(multiple):
        raise ValueError("metric and multiple must be finite")
    return metric * multiple

def peer_median(series: pd.Series) -> float:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return np.nan
    return float(values.median())

def peer_mean(series: pd.Series) -> float:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return np.nan
    return float(values.mean())

def peer_multiple_summary(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return pd.DataFrame({
        "mean": frame[columns].mean(),
        "median": frame[columns].median(),
        "min": frame[columns].min(),
        "max": frame[columns].max(),
        "count": frame[columns].count(),
    })
