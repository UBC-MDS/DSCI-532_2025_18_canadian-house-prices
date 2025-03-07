import dash_bootstrap_components as dbc
from dash import html, dcc

def create_sidebar(df):
    return dbc.Col([
        html.H3("Filters", className="mb-4", style={"color": "#FFFFFF"}),
        # City Dropdown Menu
        dbc.Row([
            html.H5("City", className="mb-4", style={"color": "#FFFFFF"}),
            dcc.Dropdown(
                id="city-filter",
                options=[{"label": city, "value": city} for city in df["City"].unique()],
                multi=True,
                placeholder="Select City",
                value=["Vancouver", "Toronto", "Montreal", "Ottawa"]
            )
        ], className="mb-4"),
        # Province Multi-Select Dropdown
        dbc.Row([
            html.H5("Province", className="mb-4", style={"color": "#FFFFFF"}),
            dcc.Dropdown(
                id="province-filter",
                options=[{"label": province, "value": province} for province in df["Province"].unique()],
                multi=True,
                placeholder="Select Province"
            )
        ], className="mb-4"),
        # Bedrooms Range Slider
        dbc.Row([
            html.H5("Bedrooms", className="mb-4", style={"color": "#FFFFFF"}),
            dcc.RangeSlider(
                id="bedrooms-slider",
                min=df["Number_Beds"].min(),
                max=df["Number_Beds"].max(),
                step=1,
                marks={i: str(i) for i in range(df["Number_Beds"].min(), df["Number_Beds"].max() + 1)},
                tooltip={"always_visible": True, "placement": "bottom"},
                value=[df["Number_Beds"].min(), df["Number_Beds"].max()]
            )
        ], className="mb-4"),
        # Bathrooms Range Slider
        dbc.Row([
            html.H5("Bathrooms", className="mb-4", style={"color": "#FFFFFF"}),
            dcc.RangeSlider(
                id="bathrooms-slider",
                min=df["Number_Baths"].min(),
                max=df["Number_Baths"].max(),
                step=1,
                marks={i: str(i) for i in range(df["Number_Baths"].min(), df["Number_Baths"].max() + 1)},
                tooltip={"always_visible": True, "placement": "bottom"},
                value=[df["Number_Baths"].min(), df["Number_Baths"].max()]
            )
        ], className="mb-4"),
        # Reset Filters Button
        dbc.Row([
            dbc.Col(
                dbc.Button(
                    "Reset Filters",
                    id="reset-button",
                    color="primary",
                    style={"background-color": "#0E1731", "color": "#FFFFFF", "border-color": "#053FA8", "font-size": "20px"},
                    className="mt-2"
                ),
                width=12
            )
        ], className="mb-4")
    ], width=2, style={
        "background-color": "#053FA8",
        "padding": "20px",
        "box-shadow": "2px 0 5px 0 rgba(0,0,0,0.2)"
    })