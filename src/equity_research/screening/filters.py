"""Eligibility filters for research universes."""
from __future__ import annotations
import pandas as pd

def require_non_null(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    if not columns:
        return pd.Series(True, index=frame.index)
    missing = [c for c in columns if c not in frame.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return frame[columns].notna().all(axis=1)

def numeric_range(frame: pd.DataFrame, column: str, minimum: float | None = None, maximum: float | None = None) -> pd.Series:
    if column not in frame.columns:
        raise ValueError(f"Missing column: {column}")
    values = pd.to_numeric(frame[column], errors="coerce")
    mask = values.notna()
    if minimum is not None: mask &= values >= minimum
    if maximum is not None: mask &= values <= maximum
    return mask

def apply_filters(frame: pd.DataFrame, filters: list[pd.Series]) -> pd.DataFrame:
    mask = pd.Series(True, index=frame.index)
    for current in filters:
        if not current.index.equals(frame.index):
            raise ValueError("Filter index must match frame index.")
        mask &= current.fillna(False)
    return frame.loc[mask].copy()
