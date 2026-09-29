"""Run the frozen NIFTY 500 momentum baseline on prepared point-in-time data."""
from __future__ import annotations

import pandas as pd

from equity_research.backtesting.metrics import (
    annualized_volatility,
    cagr,
    max_drawdown,
    sharpe_ratio,
    total_return,
)
from equity_research.research.cross_sectional import (
    momentum_12m_signal,
    run_cross_sectional_backtest,
)


def run_baseline(
    prices: pd.DataFrame,
    asset_returns: pd.DataFrame,
    risk_free_rate: float = 0.06,
    cost_rate: float = 0.0005,
    top_n: int = 20,
    lookback: int = 252,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run the frozen baseline and return weights plus daily backtest output."""
    target, result = run_cross_sectional_backtest(
        prices=prices,
        asset_returns=asset_returns,
        signal_function=lambda history: momentum_12m_signal(history, lookback=lookback),
        top_n=top_n,
        cost_rate=cost_rate,
    )

    metrics = pd.Series(
        {
            "TotalReturn": total_return(result["NetReturn"]),
            "CAGR": cagr(result["NetReturn"]),
            "AnnualizedVolatility": annualized_volatility(result["NetReturn"]),
            "Sharpe": sharpe_ratio(
                result["NetReturn"], risk_free_rate=risk_free_rate
            ),
            "MaxDrawdown": max_drawdown(result["NetReturn"]),
            "AverageTurnover": result["Turnover"].mean(),
            "TotalTransactionCost": result["TransactionCost"].sum(),
        },
        name="Momentum12M",
    ).to_frame()
    return target, result.join(metrics.T, how="left")


def load_price_matrix(frame: pd.DataFrame) -> pd.DataFrame:
    """Convert a point-in-time OHLCV table to a daily adjusted-close matrix.

    Expected columns: Date, Symbol, Adj Close.
    """
    required = {"Date", "Symbol", "Adj Close"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    tidy = frame.copy()
    tidy["Date"] = pd.to_datetime(tidy["Date"])
    tidy["Adj Close"] = pd.to_numeric(tidy["Adj Close"], errors="coerce")
    return (
        tidy.dropna(subset=["Date", "Symbol", "Adj Close"])
        .pivot_table(index="Date", columns="Symbol", values="Adj Close", aggfunc="last")
        .sort_index()
    )
