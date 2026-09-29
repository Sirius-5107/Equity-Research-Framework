import pandas as pd
import pytest

from equity_research.data.pit import apply_pit_membership, filter_flagged_pit_rows, load_membership_history, membership_mask

def test_membership_intervals_are_half_open(tmp_path):
    path = tmp_path / "membership.csv"
    pd.DataFrame({"index_name": ["Nifty 500"], "symbol": ["AAA"], "valid_from": ["2024-01-02"], "valid_to": ["2024-01-04"]}).to_csv(path, index=False)
    membership = load_membership_history(path)
    dates = pd.date_range("2024-01-01", periods=5)
    mask = membership_mask(dates, pd.Index(["AAA"]), membership)
    assert list(mask["AAA"]) == [False, True, True, False, False]

def test_open_interval_remains_eligible():
    membership = pd.DataFrame({"index_name": ["Nifty 500"], "symbol": ["AAA"], "valid_from": pd.to_datetime(["2024-01-02"]), "valid_to": pd.to_datetime([pd.NaT])})
    dates = pd.date_range("2024-01-01", periods=3)
    mask = membership_mask(dates, pd.Index(["AAA"]), membership)
    assert list(mask["AAA"]) == [False, True, True]

def test_apply_pit_membership_masks_non_members():
    dates = pd.date_range("2024-01-01", periods=3)
    prices = pd.DataFrame({"AAA": [10.0, 11.0, 12.0], "BBB": [20.0, 21.0, 22.0]}, index=dates)
    membership = pd.DataFrame({"index_name": ["Nifty 500"], "symbol": ["AAA"], "valid_from": pd.to_datetime(["2024-01-02"]), "valid_to": pd.to_datetime([pd.NaT])})
    result = apply_pit_membership(prices, membership)
    assert pd.isna(result.loc[dates[0], "AAA"])
    assert result.loc[dates[1], "AAA"] == pytest.approx(11.0)
    assert result["BBB"].isna().all()

def test_filter_flagged_rows_keeps_only_true_rows():
    frame = pd.DataFrame({"symbol": ["AAA", "BBB"], "date": pd.to_datetime(["2024-01-02", "2024-01-02"]), "is_nifty500_constituent": [True, False]})
    result = filter_flagged_pit_rows(frame)
    assert result["symbol"].tolist() == ["AAA"]
