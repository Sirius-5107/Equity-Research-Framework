import pandas as pd
import pytest

from equity_research.data.universe import (
    normalize_symbol,
    symbols_from_frame,
    symbols_to_yfinance,
    to_yfinance_symbol,
)


def test_normalize_symbol():
    assert normalize_symbol("  reliance.ns ") == "RELIANCE"


def test_to_yfinance_symbol():
    assert to_yfinance_symbol("RELIANCE") == "RELIANCE.NS"


def test_symbols_are_unique_and_sorted():
    frame = pd.DataFrame({"Symbol": ["TCS", "RELIANCE", "TCS", "INFY.NS"]})
    assert symbols_from_frame(frame) == ["INFY", "RELIANCE", "TCS"]
    assert symbols_to_yfinance(["TCS", "INFY", "TCS"]) == ["INFY.NS", "TCS.NS"]


def test_symbols_from_frame_requires_symbol():
    with pytest.raises(ValueError):
        symbols_from_frame(pd.DataFrame({"Ticker": ["TCS"]}))
