"""High-level factor-to-backtest research pipeline."""
from __future__ import annotations

import pandas as pd

from .backtesting.engine import run_backtest
from .backtesting.portfolio import equal_weight
from .factors.scoring import weighted_score
from .screening.screener import ScreenSpec, screen


def build_factor_score(
    frame: pd.DataFrame,
    weights: dict[str, float],
    higher_is_better: dict[str, bool] | None = None,
) -> pd.Series:
    """Create a cross-sectional composite score from factor columns."""
    return weighted_score(frame, weights, higher_is_better)


def build_target_weights(
    frame: pd.DataFrame,
    top_n: int = 20,
    score_column: str = "score",
) -> pd.Series:
    """Select the top-ranked names and assign equal weights."""
    screened = screen(
        frame,
        ScreenSpec(required_columns=[score_column], top_n=top_n, score_column=score_column),
    )
    return equal_weight(screened.index)


def run_factor_backtest(
    factor_frames: pd.DataFrame,
    asset_returns: pd.DataFrame,
    factor_weights: dict[str, float],
    higher_is_better: dict[str, bool] | None = None,
    top_n: int = 20,
    cost_rate: float = 0.0005,
) -> tuple[pd.Series, pd.DataFrame]:
    """Build scores, select a portfolio, and run a one-period-lagged backtest.

    This helper is intended for a single cross-section. For repeated dated
    cross-sections, construct a target-weight DataFrame and call run_backtest.
    """
    scored = factor_frames.copy()
    scored["score"] = build_factor_score(scored, factor_weights, higher_is_better)
    weights = build_target_weights(scored, top_n=top_n)
    target = pd.DataFrame(0.0, index=asset_returns.index, columns=asset_returns.columns)
    if len(target.index):
        target.iloc[0] = weights.reindex(target.columns).fillna(0.0)
    return weights, run_backtest(asset_returns, target, cost_rate=cost_rate)
