import pandas as pd
import pytest
from equity_research.valuation import (
    enterprise_value, equity_value, implied_share_price, peer_median,
    present_value, terminal_value_gordon, two_way_sensitivity,
)

def test_present_value():
    assert present_value(pd.Series([100.0]), 0.10) == pytest.approx(90.9091, rel=1e-4)

def test_terminal_value_requires_spread():
    with pytest.raises(ValueError):
        terminal_value_gordon(100.0, 0.05, 0.05)

def test_dcf_bridge():
    fcf = pd.Series([100.0, 110.0])
    tv = terminal_value_gordon(110.0, 0.03, 0.10)
    ev = enterprise_value(fcf, 0.10, tv)
    eq = equity_value(ev, debt=100.0, cash=40.0)
    assert implied_share_price(eq, 10.0) > 0

def test_peer_median():
    assert peer_median(pd.Series([10, 20, 30])) == 20

def test_sensitivity():
    result = two_way_sensitivity([.08, .10], [1, 2], lambda a, b: a + b)
    assert result.loc[.10, 2] == pytest.approx(2.10)
