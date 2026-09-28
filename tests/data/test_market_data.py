import pandas as pd
import pytest

from equity_research.data import market_data


def test_download_ohlcv_normalizes_ticker(monkeypatch):
    index = pd.date_range("2026-01-01", periods=2, freq="D")
    columns = pd.MultiIndex.from_product(
        [["TCS.NS"], ["Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    )
    raw = pd.DataFrame(
        [[100, 102, 99, 101, 101, 1000], [101, 103, 100, 102, 102, 1100]],
        index=index,
        columns=columns,
    )
    monkeypatch.setattr(market_data.yf, "download", lambda **_: raw)
    result = market_data.download_ohlcv([" tcs "], "2026-01-01", "2026-01-03")
    assert list(result.columns) == market_data.OHLCV_COLUMNS
    assert result["Symbol"].unique().tolist() == ["TCS"]
    assert result["Close"].tolist() == [101, 102]


def test_download_ohlcv_rejects_invalid_date_range():
    with pytest.raises(ValueError):
        market_data.download_ohlcv(["TCS"], "2026-02-01", "2026-01-01")
