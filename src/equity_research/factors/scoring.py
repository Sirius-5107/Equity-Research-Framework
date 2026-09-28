"""Cross-sectional factor scoring utilities."""
from __future__ import annotations
import pandas as pd

def percentile_score(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Convert a factor to percentile ranks in [0, 1], preserving NaNs."""
    score = series.rank(pct=True, method="average")
    return score if higher_is_better else 1.0 - score

def weighted_score(
    factors: pd.DataFrame,
    weights: dict[str, float],
    higher_is_better: dict[str, bool] | None = None,
) -> pd.Series:
    """Combine independently scored factors using normalized non-negative weights."""
    if not weights:
        raise ValueError("At least one factor weight is required.")
    if any(weight < 0 for weight in weights.values()):
        raise ValueError("Factor weights must be non-negative.")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("At least one factor weight must be positive.")

    scores = {}
    for name, weight in weights.items():
        if name not in factors.columns:
            raise ValueError(f"Missing factor: {name}")
        direction = True if higher_is_better is None else higher_is_better.get(name, True)
        scores[name] = percentile_score(factors[name], direction)
    return pd.DataFrame(scores).mul(pd.Series(weights)).sum(axis=1, min_count=1) / total
