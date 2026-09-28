import numpy as np
import pandas as pd
import pytest
from equity_research.data.fundamentals import cagr, debt_equity, fcf_margin, latest_value, operating_margin, roe

def statements():
    income = pd.DataFrame({"2025": [120., 30., 35.], "2024": [100., 20., 25.]}, index=["Total Revenue", "Net Income", "Operating Income"])
    balance = pd.DataFrame({"2025": [60., 120.], "2024": [50., 100.]}, index=["Total Debt", "Stockholders Equity"])
    cashflow = pd.DataFrame({"2025": [12.], "2024": [10.]}, index=["Free Cash Flow"])
    return income, balance, cashflow

def test_latest_value():
    assert latest_value(pd.Series([120., 100.], index=["2025", "2024"])) == 120.

def test_debt_equity():
    _, bs, _ = statements()
    assert debt_equity(bs) == pytest.approx(.5)

def test_operating_margin():
    income, _, _ = statements()
    assert operating_margin(income) == pytest.approx(35 / 120 * 100)

def test_roe():
    income, bs, _ = statements()
    assert roe(income, bs) == pytest.approx(25.)

def test_fcf_margin():
    income, _, cf = statements()
    assert fcf_margin(income, cf) == pytest.approx(10.)

def test_cagr():
    assert cagr(pd.Series([100., 110., 121.])) == pytest.approx(.10)
    assert np.isnan(cagr(pd.Series([100., 0., 121.])))
