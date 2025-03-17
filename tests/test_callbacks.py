import pytest
import pandas as pd
from src.callbacks.charts import get_filtered_data

@pytest.fixture
def sample_df():
    """Fixture to create a sample DataFrame for filtering."""
    return pd.DataFrame({
        "City": ["Vancouver", "Toronto", "Montreal"],
        "Province": ["BC", "ON", "QC"],
        "Number_Beds": [2, 3, 4],
        "Number_Baths": [1, 2, 3],
        "Price": [800000, 900000, 750000]
    })

def test_get_filtered_data(sample_df, monkeypatch):
    """Test the get_filtered_data function with sample filters."""
    
    # Patch the global df to use the sample dataframe
    monkeypatch.setattr("src.callbacks.charts.df", sample_df)

    filtered_data = get_filtered_data(("Vancouver",), ("BC",), (2, 4), (1, 3))
    
    assert not filtered_data.empty
    assert all(filtered_data["City"] == "Vancouver")
    assert all(filtered_data["Province"] == "BC")
    assert all(filtered_data["Number_Beds"].between(2, 4))
    assert all(filtered_data["Number_Baths"].between(1, 3))
