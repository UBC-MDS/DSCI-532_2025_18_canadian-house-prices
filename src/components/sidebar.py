from dash import dcc, html
import dash_bootstrap_components as dbc
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.data_loader import load_data

df = load_data()

sidebar = html.Div([
    html.H3("Filters", className="mb-4", style={"color": "#FFFFFF"}),

    html.H5("City", className="mb-4", style={"color": "#FFFFFF"}),
    dcc.Dropdown(
        id="city-filter",
        options=[{"label": city, "value": city} for city in df["City"].unique()],
        multi=True,
        placeholder="Select City",
        value=["Vancouver", "Toronto", "Montreal", "Ottawa"]
    ),

    html.H5("Province", className="mb-4", style={"color": "#FFFFFF"}),
    dcc.Dropdown(
        id="province-filter",
        options=[{"label": province, "value": province} for province in df["Province"].unique()],
        multi=True,
        placeholder="Select Province"
    ),

    html.H5("Bedrooms", className="mb-4", style={"color": "#FFFFFF"}),
    dcc.RangeSlider(
        id="bedrooms-slider",
        min=df["Number_Beds"].min(),
        max=df["Number_Beds"].max(),
        step=1,
        marks={i: str(i) for i in range(df["Number_Beds"].min(), df["Number_Beds"].max() + 1)},
        tooltip={"always_visible": True, "placement": "bottom"},
        value=[df["Number_Beds"].min(), df["Number_Beds"].max()]
    ),

    dbc.Button("Reset Filters", id="reset-button", color="primary", className="mt-2")
])
