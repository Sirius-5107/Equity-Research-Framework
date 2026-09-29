"""Portfolio construction utilities."""
from __future__ import annotations
import pandas as pd

def equal_weight(assets: pd.Index | list[str], max_positions: int | None = None) -> pd.Series:
    assets = pd.Index(assets).drop_duplicates()
    if max_positions is not None and max_positions <= 0:
        raise ValueError("max_positions must be positive")
    if max_positions is not None:
        assets = assets[:max_positions]
    if len(assets) == 0:
        return pd.Series(dtype=float)
    return pd.Series(1.0 / len(assets), index=assets, dtype=float)

def normalize_weights(weights: pd.Series) -> pd.Series:
    values = pd.to_numeric(weights, errors="coerce").fillna(0.0)
    if (values < 0).any():
        raise ValueError("long-only weights cannot be negative")
    total = float(values.sum())
    if total <= 0:
        return pd.Series(0.0, index=values.index, dtype=float)
    return values / total

def score_weighted(scores: pd.Series, max_positions: int | None = None) -> pd.Series:
    clean = pd.to_numeric(scores, errors="coerce").dropna()
    clean = clean[clean > 0].sort_values(ascending=False)
    if max_positions is not None:
        if max_positions <= 0:
            raise ValueError("max_positions must be positive")
        clean = clean.head(max_positions)
    return normalize_weights(clean)

def portfolio_return(weights: pd.Series, asset_returns: pd.Series) -> float:
    aligned = pd.concat([weights, asset_returns], axis=1).dropna()
    if aligned.empty:
        return 0.0
    return float((aligned.iloc[:, 0] * aligned.iloc[:, 1]).sum())
