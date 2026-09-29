import numpy as np
import pandas as pd
import pytest

from equity_research.backtesting import annualized_volatility, equal_weight, max_drawdown, run_backtest, sharpe_ratio, total_return, transaction_cost, turnover

def test_equal_weight():
    assert equal_weight(["A", "B"]).to_dict() == {"A": 0.5, "B": 0.5}

def test_turnover_and_cost():
    previous = pd.Series({"A": 0.5, "B": 0.5})
    target = pd.Series({"A": 1.0})
    assert turnover(previous, target) == pytest.approx(1.0)
    assert transaction_cost(1.0, 0.0005) == pytest.approx(0.0005)

def test_metrics():
    returns = pd.Series([0.10, -0.05, 0.02])
    assert total_return(returns) == pytest.approx((1.1 * .95 * 1.02) - 1)
    assert max_drawdown(returns) < 0
    assert annualized_volatility(returns) > 0
    assert np.isfinite(sharpe_ratio(returns))

def test_signal_lag_and_costs():
    dates = pd.date_range("2026-01-01", periods=3, freq="D")
    asset_returns = pd.DataFrame({"A": [0.00, 0.10, 0.20]}, index=dates)
    weights = pd.DataFrame({"A": [1.0, 1.0, 1.0]}, index=dates)
    result = run_backtest(asset_returns, weights, cost_rate=0.001)
    assert result.index.tolist() == list(dates[1:])
    assert result.iloc[0]["GrossReturn"] == pytest.approx(0.10)
    assert result.iloc[0]["TransactionCost"] == pytest.approx(0.001)
    assert result.iloc[0]["NetReturn"] == pytest.approx(0.099)

def test_empty_portfolio_has_no_return():
    dates = pd.date_range("2026-01-01", periods=2, freq="D")
    asset_returns = pd.DataFrame({"A": [0.0, 0.1]}, index=dates)
    weights = pd.DataFrame({"A": [0.0, 0.0]}, index=dates)
    result = run_backtest(asset_returns, weights)
    assert result.iloc[0]["NetReturn"] == 0.0
