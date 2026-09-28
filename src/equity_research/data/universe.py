"""Universe loaders for Indian equity research.

The framework uses exchange-maintained constituent lists where practical and
keeps symbol normalization separate from market-data retrieval.
"""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

NIFTY_500_URL = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"


def normalize_symbol(symbol: str) -> str:
    """Normalize an NSE symbol for use by the framework and yfinance."""
    return str(symbol).strip().upper().removesuffix(".NS")


def to_yfinance_symbol(symbol: str) -> str:
    """Convert an NSE symbol to its Yahoo Finance representation."""
    return f"{normalize_symbol(symbol)}.NS"


def load_nifty500(url: str = NIFTY_500_URL) -> pd.DataFrame:
    """Load the current NIFTY 500 constituent list from NSE."""
    frame = pd.read_csv(url)
    if "Symbol" not in frame.columns:
        raise ValueError("NIFTY 500 constituent file does not contain 'Symbol'.")
    frame = frame.copy()
    frame["Symbol"] = frame["Symbol"].map(normalize_symbol)
    frame = frame.loc[frame["Symbol"].ne("")]
    return frame.drop_duplicates(subset="Symbol").reset_index(drop=True)


def symbols_from_frame(frame: pd.DataFrame) -> list[str]:
    """Extract normalized symbols from a constituent dataframe."""
    if "Symbol" not in frame.columns:
        raise ValueError("Constituent dataframe must contain a 'Symbol' column.")
    return sorted({normalize_symbol(s) for s in frame["Symbol"] if str(s).strip()})


def symbols_to_yfinance(symbols: Iterable[str]) -> list[str]:
    """Convert an iterable of NSE symbols to sorted Yahoo Finance symbols."""
    return sorted({to_yfinance_symbol(symbol) for symbol in symbols})
