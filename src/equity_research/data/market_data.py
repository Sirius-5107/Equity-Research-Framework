"""Market-data acquisition and normalization via Yahoo Finance."""

from __future__ import annotations

import logging
from collections.abc import Sequence

import pandas as pd
import yfinance as yf

from .universe import normalize_symbol

LOGGER = logging.getLogger(__name__)

OHLCV_COLUMNS = ["Date", "Symbol", "Open", "High", "Low", "Close", "Adj Close", "Volume"]


def download_ohlcv(symbols: Sequence[str], start: str, end: str) -> pd.DataFrame:
    """Download OHLCV data and return a tidy long-format dataframe."""
    normalized = sorted({normalize_symbol(symbol) for symbol in symbols})
    if not normalized:
        raise ValueError("At least one symbol is required.")
    if pd.Timestamp(start) >= pd.Timestamp(end):
        raise ValueError("'start' must be earlier than 'end'.")

    yahoo_symbols = [f"{symbol}.NS" for symbol in normalized]
    raw = yf.download(
        tickers=yahoo_symbols,
        start=start,
        end=end,
        group_by="ticker",
        auto_adjust=False,
        progress=False,
    )
    if raw.empty:
        raise ValueError("Yahoo Finance returned no market data.")

    records: list[pd.DataFrame] = []
    available = set(raw.columns.get_level_values(0)) if isinstance(raw.columns, pd.MultiIndex) else set()

    for symbol, yahoo_symbol in zip(normalized, yahoo_symbols):
        if isinstance(raw.columns, pd.MultiIndex):
            if yahoo_symbol not in available:
                LOGGER.warning("No data returned for %s", yahoo_symbol)
                continue
            frame = raw[yahoo_symbol].copy()
        else:
            frame = raw.copy()

        frame = frame.dropna(how="all")
        if frame.empty:
            LOGGER.warning("No usable rows returned for %s", yahoo_symbol)
            continue

        frame["Symbol"] = symbol
        records.append(frame)

    if not records:
        raise ValueError("No usable ticker data was returned.")

    combined = pd.concat(records).reset_index()
    if "index" in combined.columns and "Date" not in combined.columns:
        combined = combined.rename(columns={"index": "Date"})

    for column in OHLCV_COLUMNS:
        if column not in combined.columns:
            combined[column] = pd.NA

    combined = combined[OHLCV_COLUMNS]
    combined["Date"] = pd.to_datetime(combined["Date"])
    for column in ["Open", "High", "Low", "Close", "Adj Close"]:
        combined[column] = pd.to_numeric(combined[column], errors="coerce")
    combined["Volume"] = pd.to_numeric(combined["Volume"], errors="coerce").astype("Int64")

    return (
        combined.dropna(subset=["Date", "Symbol"])
        .sort_values(["Date", "Symbol"])
        .drop_duplicates(["Date", "Symbol"])
        .reset_index(drop=True)
    )
