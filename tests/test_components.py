import pytest
import pandas as pd
import dash_bootstrap_components as dbc
from dash.development.base_component import Component
from src.components.charts import create_map_card, create_chart1_card, create_chart2_card, create_chart3_card
from src.components.sidebar import create_sidebar
from src.components.summary_cards import create_summary_cards

@pytest.fixture
def sample_df():
    """Fixture to create a sample DataFrame for testing."""
    return pd.DataFrame({
        "Province": ["BC", "ON"],
        "City": ["Vancouver", "Toronto"],
        "Number_Beds": [2, 3],
        "Number_Baths": [1, 2]
    })

def test_map_card():
    """Test if the map card returns a valid Dash component."""
    assert isinstance(create_map_card(), Component)

def test_chart1_card():
    """Test if chart1 card returns a valid Dash component."""
    assert isinstance(create_chart1_card(), Component)

def test_chart2_card():
    """Test if chart2 card returns a valid Dash component."""
    assert isinstance(create_chart2_card(), Component)

def test_chart3_card():
    """Test if chart3 card returns a valid Dash component."""
    assert isinstance(create_chart3_card(), Component)

def test_sidebar(sample_df):
    """Test if sidebar returns a valid Dash component."""
    assert isinstance(create_sidebar(sample_df), Component)

def test_summary_cards():
    """Test if summary cards return a valid Dash component."""
    assert isinstance(create_summary_cards(), Component)
