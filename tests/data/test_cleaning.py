import numpy as np
import pandas as pd
import pytest

from equity_research.data.cleaning import drop_duplicate_symbols, median_impute_numeric


def test_drop_duplicate_symbols():
    frame = pd.DataFrame({"Symbol": ["TCS", "TCS", "INFY"], "Value": [1, 2, 3]})
    result = drop_duplicate_symbols(frame)
    assert result["Symbol"].tolist() == ["TCS", "INFY"]


def test_median_imputation_does_not_fill_all_missing_column():
    frame = pd.DataFrame({"A": [1.0, np.nan, 3.0], "B": [np.nan, np.nan, np.nan]})
    result = median_impute_numeric(frame)
    assert result["A"].tolist() == [1.0, 2.0, 3.0]
    assert result["B"].isna().all()


def test_cleaning_requires_symbol():
    with pytest.raises(ValueError):
        drop_duplicate_symbols(pd.DataFrame({"Ticker": ["TCS"]}))
