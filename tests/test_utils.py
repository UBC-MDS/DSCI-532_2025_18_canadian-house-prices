import pytest
import pandas as pd
from src.utils.data_loader import load_data

def test_load_data_structure():
    df = load_data()
    assert isinstance(df, pd.DataFrame)
    expected_columns = {"City", "Province", "Number_Beds", "Number_Baths", "Price"}
    assert expected_columns.issubset(df.columns)

def test_load_data_not_empty():
    df = load_data()
    assert not df.empty
