import numpy as np
import pandas as pd
import pytest
from equity_research.factors.momentum import total_return
from equity_research.factors.scoring import percentile_score, weighted_score
from equity_research.factors.value import earnings_yield

def test_earnings_yield():
    df = pd.DataFrame({"Earnings": [10., 20.], "MarketCap": [100., 200.]})
    assert earnings_yield(df).tolist() == [0.1, 0.1]

def test_total_return():
    prices = pd.DataFrame({"A": [100., 110., 121.], "B": [100., 90., 81.]})
    result = total_return(prices, 2)
    assert result.iloc[-1].to_dict() == {"A": pytest.approx(.21), "B": pytest.approx(-.19)}

def test_volatility():
    from equity_research.factors.volatility import annualized_volatility
    returns = pd.DataFrame({"A": [0.01, -0.01, 0.01]})
    assert annualized_volatility(returns, 252)["A"] > 0

def test_percentile_direction():
    s = pd.Series([1., 2., 3.])
    assert percentile_score(s).iloc[-1] == 1
    assert percentile_score(s, False).iloc[-1] == 0

def test_weighted_score():
    factors = pd.DataFrame({"quality": [1., 2., 3.], "value": [3., 2., 1.]})
    score = weighted_score(factors, {"quality": .5, "value": .5})
    assert score.iloc[0] == pytest.approx(.5)
    assert score.iloc[1] == pytest.approx(.5)
    assert score.iloc[2] == pytest.approx(.5)
