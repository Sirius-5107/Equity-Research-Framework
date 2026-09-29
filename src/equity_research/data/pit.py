"""Point-in-time universe eligibility helpers for historical equity research."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

def load_membership_history(path: str | Path, index_name: str = "Nifty 500") -> pd.DataFrame:
    """Load half-open NSE index membership intervals for one index."""
    frame = pd.read_csv(path, parse_dates=["valid_from", "valid_to"])
    required = {"index_name", "symbol", "valid_from", "valid_to"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required membership columns: {sorted(missing)}")
    frame = frame.loc[frame["index_name"].eq(index_name)].copy()
    frame["symbol"] = frame["symbol"].astype(str).str.strip().str.upper()
    frame["valid_from"] = pd.to_datetime(frame["valid_from"])
    frame["valid_to"] = pd.to_datetime(frame["valid_to"])
    return frame.sort_values(["valid_from", "symbol"]).reset_index(drop=True)

def membership_mask(dates: pd.DatetimeIndex, symbols: pd.Index, membership: pd.DataFrame) -> pd.DataFrame:
    """Return a date x symbol boolean PIT-membership matrix."""
    dates = pd.DatetimeIndex(dates)
    symbols = pd.Index(symbols).astype(str).str.strip().str.upper()
    result = pd.DataFrame(False, index=dates, columns=symbols)
    for row in membership.itertuples(index=False):
        start = pd.Timestamp(row.valid_from)
        end = pd.Timestamp(row.valid_to) if pd.notna(row.valid_to) else None
        date_mask = dates >= start
        if end is not None:
            date_mask &= dates < end
        if row.symbol in result.columns:
            result.loc[date_mask, row.symbol] = True
    return result

def apply_pit_membership(prices: pd.DataFrame, membership: pd.DataFrame) -> pd.DataFrame:
    """Mask non-constituent prices while preserving the full date/symbol grid."""
    if not isinstance(prices.index, pd.DatetimeIndex):
        raise TypeError("prices index must be a DatetimeIndex")
    return prices.where(membership_mask(prices.index, prices.columns, membership))

def filter_flagged_pit_rows(frame: pd.DataFrame, flag_column: str = "is_nifty500_constituent") -> pd.DataFrame:
    """Filter a long-form PIT price table using an explicit membership flag."""
    if flag_column not in frame.columns:
        raise ValueError(f"Missing PIT flag column: {flag_column}")
    return frame.loc[frame[flag_column].fillna(False).astype(bool)].copy()
