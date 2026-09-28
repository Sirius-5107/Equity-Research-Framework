"""Cross-sectional ranking utilities."""
from __future__ import annotations
import pandas as pd

def rank_factor(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    return series.rank(ascending=not higher_is_better, method="min", na_option="bottom")

def rank_by_score(frame: pd.DataFrame, score_column: str = "score", ascending: bool = False) -> pd.DataFrame:
    if score_column not in frame.columns:
        raise ValueError(f"Missing score column: {score_column}")
    return frame.sort_values(score_column, ascending=ascending, kind="mergesort").copy()

def top_n(frame: pd.DataFrame, n: int, score_column: str = "score") -> pd.DataFrame:
    if n <= 0: raise ValueError("n must be positive")
    return rank_by_score(frame, score_column).head(n).copy()
