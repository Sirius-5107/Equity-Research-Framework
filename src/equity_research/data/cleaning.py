"""Generic data-cleaning helpers used by screening and factor pipelines."""

from __future__ import annotations

import numpy as np
import pandas as pd


def drop_duplicate_symbols(df: pd.DataFrame, symbol_column: str = "Symbol") -> pd.DataFrame:
    """Keep the first observation per symbol."""
    if symbol_column not in df.columns:
        raise ValueError(f"Missing required column: {symbol_column}")
    return df.drop_duplicates(subset=symbol_column).reset_index(drop=True)


def median_impute_numeric(
    df: pd.DataFrame,
    *,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """Median-impute selected numeric columns when a finite median exists."""
    result = df.copy()
    numeric = result.select_dtypes(include=np.number).columns.tolist() if columns is None else columns
    for column in numeric:
        if column not in result.columns:
            raise ValueError(f"Missing required column: {column}")
        median = result[column].median(skipna=True)
        if pd.notna(median):
            result[column] = result[column].fillna(median)
    return result
