"""Simple signal-to-portfolio backtesting engine."""
from __future__ import annotations
import pandas as pd
from .costs import transaction_cost, turnover
from .portfolio import normalize_weights, portfolio_return

def run_backtest(asset_returns: pd.DataFrame, target_weights: pd.DataFrame, cost_rate: float = 0.0005) -> pd.DataFrame:
    """Run a long-only backtest with one-period signal lag."""
    if not asset_returns.index.equals(target_weights.index):
        raise ValueError("asset_returns and target_weights must share the same index")
    rows = []
    previous = pd.Series(dtype=float)
    for i in range(len(asset_returns) - 1):
        period_date = asset_returns.index[i + 1]
        weights = normalize_weights(target_weights.iloc[i])
        gross = portfolio_return(weights, asset_returns.iloc[i + 1])
        traded = turnover(previous, weights)
        cost = transaction_cost(traded, cost_rate)
        rows.append((period_date, gross, traded, cost, gross - cost))
        previous = weights
    return pd.DataFrame(rows, columns=["Date", "GrossReturn", "Turnover", "TransactionCost", "NetReturn"]).set_index("Date")
