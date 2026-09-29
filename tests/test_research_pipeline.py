import pandas as pd
import pytest

from equity_research.research_pipeline import build_factor_score, build_target_weights

def test_factor_score_and_direction():
    frame = pd.DataFrame({"value": [1.0, 2.0, 3.0], "quality": [3.0, 2.0, 1.0]}, index=["A","B","C"])
    score = build_factor_score(frame, {"value": 0.5, "quality": 0.5}, {"value": True, "quality": False})
    assert score["A"] == pytest.approx(0.5)
    assert score["C"] == pytest.approx(0.5)

def test_top_n_equal_weight():
    frame = pd.DataFrame({"score": [0.9, 0.7, 0.2]}, index=["A","B","C"])
    weights = build_target_weights(frame, top_n=2)
    assert weights.to_dict() == {"A": 0.5, "B": 0.5}
