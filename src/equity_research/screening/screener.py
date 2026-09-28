"""Configurable stock-screening pipeline."""
from __future__ import annotations
from dataclasses import dataclass, field
import pandas as pd
from .filters import apply_filters
from .ranking import top_n

@dataclass(frozen=True)
class ScreenSpec:
    required_columns: list[str] = field(default_factory=list)
    top_n: int = 20
    score_column: str = "score"

def screen(frame: pd.DataFrame, spec: ScreenSpec, filters: list[pd.Series] | None = None) -> pd.DataFrame:
    if frame.empty: return frame.copy()
    missing = [c for c in spec.required_columns if c not in frame.columns]
    if missing: raise ValueError(f"Missing required columns: {missing}")
    return top_n(apply_filters(frame, filters or []), spec.top_n, spec.score_column)
