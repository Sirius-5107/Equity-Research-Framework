import pandas as pd
import pytest

from equity_research.research.cross_sectional import (
    build_target_weight_history,
    monthly_rebalance_dates,
    momentum_12m_signal,
    run_cross_sectional_backtest,
)


def test_monthly_rebalance_uses_last_available_observation():
    index = pd.to_datetime(["2024-01-02", "2024-01-31", "2024-02-01", "2024-02-28"])
    assert list(monthly_rebalance_dates(index)) == list(
        pd.to_datetime(["2024-01-31", "2024-02-28"])
    )


def test_signal_cannot_see_future_prices():
    index = pd.date_range("2024-01-01", periods=4, freq="D")
    prices = pd.DataFrame(
        {"A": [100.0, 101.0, 102.0, 103.0], "B": [100.0, 99.0, 98.0, 97.0]},
        index=index,
    )

    def signal(history):
        return history.iloc[-1]

    target_a = build_target_weight_history(
        prices.iloc[:3], signal, top_n=1, rebalance_dates=[index[2]], minimum_history=1
    )
    prices_with_future_change = prices.copy()
    prices_with_future_change.loc[index[3], "A"] = 1_000_000.0
    target_b = build_target_weight_history(
        prices_with_future_change.iloc[:3], signal, top_n=1, rebalance_dates=[index[2]], minimum_history=1
    )
    pd.testing.assert_frame_equal(target_a, target_b)


def test_weights_persist_until_next_rebalance():
    index = pd.date_range("2024-01-01", periods=5, freq="D")
    prices = pd.DataFrame(
        {"A": [10, 11, 12, 13, 14], "B": [10, 9, 8, 7, 6]}, index=index, dtype=float
    )

    target = build_target_weight_history(
        prices,
        lambda history: history.iloc[-1],
        top_n=1,
        rebalance_dates=[index[1], index[3]],
    )

    assert target.loc[index[1], "A"] == pytest.approx(1.0)
    assert target.loc[index[2], "A"] == pytest.approx(1.0)
    assert target.loc[index[3], "A"] == pytest.approx(1.0)
    assert target.loc[index[4], "A"] == pytest.approx(1.0)


def test_backtest_applies_signal_on_next_period():
    index = pd.date_range("2024-01-01", periods=4, freq="D")
    prices = pd.DataFrame(
        {"A": [100.0, 101.0, 102.0, 103.0], "B": [100.0, 100.0, 100.0, 100.0]},
        index=index,
    )
    returns = prices.pct_change().fillna(0.0)
    target, result = run_cross_sectional_backtest(
        prices,
        returns,
        lambda history: pd.Series({"A": 1.0, "B": 0.0}),
        top_n=1,
        rebalance_dates=[index[1]],
        cost_rate=0.0,
    )

    assert target.loc[index[1], "A"] == pytest.approx(1.0)
    assert result.loc[index[2], "NetReturn"] == pytest.approx(returns.loc[index[2], "A"])


def test_momentum_12m_requires_lookback_history():
    prices = pd.DataFrame(
        {"A": [100.0, 110.0], "B": [100.0, 90.0]},
        index=pd.date_range("2024-01-01", periods=2),
    )
    signal = momentum_12m_signal(prices, lookback=252)
    assert signal.isna().all()
