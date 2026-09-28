import pandas as pd
import pytest
from equity_research.screening import ScreenSpec, numeric_range, require_non_null, screen

def test_numeric_range():
    frame = pd.DataFrame({"roe": [5., 12., 20.]})
    assert numeric_range(frame, "roe", minimum=10).tolist() == [False, True, True]

def test_required_columns():
    frame = pd.DataFrame({"a": [1], "b": [2]})
    assert require_non_null(frame, ["a","b"]).all()
    assert not require_non_null(frame.assign(b=[None]), ["a","b"]).all()

def test_screen_filters_then_top_n():
    frame = pd.DataFrame({"score":[.9,.8,.7,.6],"roe":[8,20,15,30]})
    result = screen(frame, ScreenSpec(required_columns=["score","roe"],top_n=2),
                    [numeric_range(frame,"roe",minimum=10)])
    assert result["score"].tolist() == [.8,.7]

def test_bad_top_n():
    with pytest.raises(ValueError): top_n = __import__("equity_research.screening", fromlist=["top_n"]).top_n(pd.DataFrame({"score":[1]}),0)
