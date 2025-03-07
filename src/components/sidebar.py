from dash import html, dcc
import dash_bootstrap_components as dbc

def sidebar(df):
    return html.Div([
        html.H3("Filters", className="mb-4", style={"color": "#FFFFFF"}),

        html.H5("City", style={"color": "#FFFFFF"}),
        dcc.Dropdown(
            id="city-filter",
            options=[{"label": city, "value": city} for city in df["City"].unique()],
            multi=True,
            placeholder="Select City",
            value=["Vancouver", "Toronto", "Montreal", "Ottawa"]
        ),

        html.H5("Province", className="mt-4", style={"color": "#FFFFFF"}),
        dcc.Dropdown(
            id="province-filter",
            options=[{"label": prov, "value": prov} for prov in df["Province"].unique()],
            multi=True,
            placeholder="Select Province"
        ),

        html.H5("Bedrooms", className="mt-4", style={"color": "#FFFFFF"}),
        dcc.RangeSlider(
            id="bedrooms-slider",
            min=df["Number_Beds"].min(),
            max=df["Number_Beds"].max(),
            step=1,
            marks={i: str(i) for i in range(df["Number_Beds"].min(), df["Number_Beds"].max() + 1)},
            tooltip={"always_visible": True},
            value=[df["Number_Beds"].min(), df["Number_Beds"].max()]
        ),

        html.H5("Bathrooms", className="mt-4", style={"color": "#FFFFFF"}),
        dcc.RangeSlider(
            id="bathrooms-slider",
            min=df["Number_Baths"].min(),
            max=df["Number_Baths"].max(),
            step=1,
            marks={i: str(i) for i in range(df["Number_Baths"].min(), df["Number_Baths"].max() + 1)},
            tooltip={"always_visible": True},
            value=[df["Number_Baths"].min(), df["Number_Baths"].max()]
        ),

        dbc.Button("Reset Filters", id="reset-button", color="primary", className="mt-4")
    ])
