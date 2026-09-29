"""Valuation sensitivity-analysis utilities."""
from __future__ import annotations
from collections.abc import Callable, Sequence
import pandas as pd

def two_way_sensitivity(
    row_values: Sequence[float],
    column_values: Sequence[float],
    evaluator: Callable[[float, float], float],
    row_name: str = "row",
    column_name: str = "column",
) -> pd.DataFrame:
    if not row_values or not column_values:
        raise ValueError("sensitivity axes cannot be empty")
    matrix = [
        [evaluator(row_value, column_value) for column_value in column_values]
        for row_value in row_values
    ]
    return pd.DataFrame(
        matrix,
        index=pd.Index(row_values, name=row_name),
        columns=pd.Index(column_values, name=column_name),
    )
