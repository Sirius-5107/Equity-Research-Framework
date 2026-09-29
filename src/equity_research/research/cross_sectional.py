"""Dated cross-sectional research and backtesting workflows."""
from __future__ import annotations

from collections.abc import Callable, Iterable

import pandas as pd

from ..backtesting.engine import run_backtest
from ..backtesting.portfolio import equal_weight
from ..factors.momentum import cross_sectional_momentum
from ..screening.screener import ScreenSpec, screen

SignalFunction = Callable[[pd.DataFrame], pd.Series]


def monthly_rebalance_dates(index: pd.Index) -> pd.DatetimeIndex:
    """Return the last available observation in each calendar month."""
    dates = pd.DatetimeIndex(index).sort_values().unique()
    if len(dates) == 0:
        return dates
    frame = pd.Series(dates, index=dates)
    return pd.DatetimeIndex(frame.groupby(dates.to_period("M")).max().to_numpy())


def _select_equal_weight_portfolio(
    signal: pd.Series,
    top_n: int,
) -> pd.Series:
    """Rank one cross-section and equal-weight the top names."""
    frame = signal.rename("score").to_frame().dropna()
    screened = screen(
        frame,
        ScreenSpec(required_columns=["score"], top_n=top_n, score_column="score"),
    )
    return equal_weight(screened.index)


def build_target_weight_history(
    prices: pd.DataFrame,
    signal_function: SignalFunction,
    top_n: int,
    rebalance_dates: Iterable[pd.Timestamp] | None = None,
    minimum_history: int = 1,
) -> pd.DataFrame:
    """Build point-in-time target weights and forward-fill between rebalances.

    The signal function receives only prices through the rebalance date. No
    future observations are passed to it. Weights are zero before the first
    valid rebalance and remain unchanged until the next rebalance.
    """
    if top_n <= 0:
        raise ValueError("top_n must be positive")
    if minimum_history <= 0:
        raise ValueError("minimum_history must be positive")
    if prices.empty:
        raise ValueError("prices must not be empty")

    prices = prices.sort_index().copy()
    dates = pd.DatetimeIndex(prices.index)
    if rebalance_dates is None:
        dates = monthly_rebalance_dates(dates)
    else:
        dates = pd.DatetimeIndex(rebalance_dates).intersection(dates)

    target = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    for date in dates:
        history = prices.loc[:date]
        if len(history) < minimum_history:
            continue
        signal = signal_function(history)
        weights = _select_equal_weight_portfolio(signal, top_n)
        target.loc[date, weights.index] = weights

    # A target is a persistent portfolio instruction, not a one-day trade.
    target = target.replace([float("inf"), float("-inf")], pd.NA).fillna(0.0)
    target = target.mask(target.eq(0.0)).ffill().fillna(0.0)
    return target


def run_cross_sectional_backtest(
    prices: pd.DataFrame,
    asset_returns: pd.DataFrame,
    signal_function: SignalFunction,
    top_n: int = 20,
    cost_rate: float = 0.0005,
    rebalance_dates: Iterable[pd.Timestamp] | None = None,
    minimum_history: int = 1,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run a dated cross-sectional strategy with one-period execution lag.

    Returns the target-weight history and the existing backtest engine output.
    The two input frames must use the same daily index and asset columns.
    """
    if not prices.index.equals(asset_returns.index):
        raise ValueError("prices and asset_returns must share the same index")
    if not prices.columns.equals(asset_returns.columns):
        raise ValueError("prices and asset_returns must share the same columns")

    target = build_target_weight_history(
        prices=prices,
        signal_function=signal_function,
        top_n=top_n,
        rebalance_dates=rebalance_dates,
        minimum_history=minimum_history,
    )
    result = run_backtest(asset_returns, target, cost_rate=cost_rate)
    return target, result


def momentum_12m_signal(prices: pd.DataFrame, lookback: int = 252) -> pd.Series:
    """Trailing 12-month price momentum using 252 trading observations."""
    return cross_sectional_momentum(prices, lookback=lookback)
