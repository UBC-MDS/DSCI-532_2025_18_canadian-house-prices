import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
import pandas as pd
import plotly.express as px
import dash
import pandas as pd
from pygments.styles.dracula import background

# Load dataset
file_path = "data/processed/Cleaned_CanadianHousePrices.csv"
df = pd.read_csv(file_path).dropna()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Layout
app.layout = dbc.Container(fluid=True, children=[

    # Title
    dbc.Row([
        dbc.Col(html.H2("Canadian House Prices Dashboard", className="text-center"), width=12)
    ], className="mb-3"),

   dbc.Row([
       # Filters Panel
       dbc.Col([
           html.H3("Filters", className="mb-4"),

           # City Dropdown Menu
           dbc.Row([
               dbc.Label("City", html_for="city-filter", width=12),
               dcc.Dropdown(
                   id="city-filter",
                   options=[{"label": city, "value": city} for city in df["City"].unique()],
                   multi=True, placeholder="Select City"
               )
           ], className="mb-4"),

           # Year Slider
           dbc.Row([
               dbc.Label("Year Range", html_for="year-slider", width=12),
               dcc.RangeSlider(
                   id="year-slider",
                   min=2000, max=2020, step=1,
                   marks={i: str(i) for i in range(2000, 2021, 5)},  # Marks only for every 5 years
                   tooltip={"always_visible": True}
               )
           ], className="mb-4"),

           # Min/Max Bedrooms Input
           dbc.Row([
               dbc.Label("Bedrooms", html_for="bedrooms-min", width=12),
               dbc.Col(dbc.Input(id="bedrooms-min", type="number", placeholder="Min Bedrooms"), width=6),
               dbc.Col(dbc.Input(id="bedrooms-max", type="number", placeholder="Max Bedrooms"), width=6)
           ], className="mb-4"),

           # Min/Max Bathrooms Input
           dbc.Row([
               dbc.Label("Bathrooms", html_for="bathrooms-min", width=12),
               dbc.Col(dbc.Input(id="bathrooms-min", type="number", placeholder="Min Bathrooms"), width=6),
               dbc.Col(dbc.Input(id="bathrooms-max", type="number", placeholder="Max Bathrooms"), width=6)
           ], className="mb-4"),

           # Min/Max Sq Ft Input
           dbc.Row([
               dbc.Label("Square Footage", html_for="sqft-min", width=12),
               dbc.Col(dbc.Input(id="sqft-min", type="number", placeholder="Min Sq Ft"), width=6),
               dbc.Col(dbc.Input(id="sqft-max", type="number", placeholder="Max Sq Ft"), width=6)
           ], className="mb-4")

       ], width=2, className="bg-light p-4 rounded"),

       # Main Container
       dbc.Col([
           # Summary Stats
           dbc.Row([
               dbc.Col(html.Div(id="median-price", className="border p-2 text-center bg-light"), width=4),
               dbc.Col(html.Div(id="avg-bedrooms", className="border p-2 text-center bg-light"), width=4),
               dbc.Col(html.Div(id="price-range", className="border p-2 text-center bg-light"), width=4)
           ], className="mb-3"),

           # Charts & Map Section
           dbc.Row([
               dbc.Col(dbc.Card([
                   dbc.CardHeader("Placeholder Chart 1"),
                   dbc.CardBody(dcc.Graph(id="chart1", style={"height": "400px", "padding": "5px", "background-color": "lightblue"}))
               ], className="m-1"), width=6),

               dbc.Col(dbc.Card([
                   dbc.CardHeader("Placeholder Chart 2"),
                   dbc.CardBody(dcc.Graph(id="chart2", style={"height": "400px"}))
               ], className="m-1"), width=6)
           ], className="mb-1"),

           dbc.Row([
               dbc.Col(dbc.Card([
                   dbc.CardHeader("Placeholder Chart 3"),
                   dbc.CardBody(dcc.Graph(id="chart3", style={"height": "400px"}))
               ], className="m-1"), width=6),

               dbc.Col(dbc.Card([
                   dbc.CardHeader("Map"),
                   dbc.CardBody(dcc.Graph(id="map", style={"height": "400px"}))
               ], className="m-1"), width=6)
           ], className="mb-1")
       ], className="mb-3")
   ])
])

# Callbacks
@app.callback(
    [Output("median-price", "children"),
     Output("avg-bedrooms", "children"),
     Output("price-range", "children"),
     Output("chart1", "figure"),
     Output("chart2", "figure"),
     Output("chart3", "figure"),
     Output("map", "figure")],
    Input("chart1", "id")
)
def update_dashboard(_):
    # Summary Stats
    median_price = df["Price"].median()
    avg_bedrooms = df["Number_Beds"].mean()
    min_price = df["Price"].min()
    max_price = df["Price"].max()

    # Placeholder Charts
    chart1 = px.bar(x=["A", "B", "C"], y=[10, 20, 15], title="Chart 1")
    chart1.update_layout(
        # Customize the style of the plot
        margin = dict(l=30, r=30, t=60, b=60)
    )
    chart2 = px.box(x=["X", "Y", "Z"], y=[5, 15, 10], title="Chart 2")
    chart2.update_layout(
        # Customize the style of the plot
        margin = dict(l=30, r=30, t=60, b=60)
    )
    chart3 = px.scatter(x=["D", "E", "F"], y=[12, 9, 14], title="Chart 3")
    chart3.update_layout(
        # Customize the style of the plot
        margin = dict(l=30, r=30, t=60, b=60)
    )
    # Map
    map_fig = px.scatter_mapbox(
        lat=df["Latitude"], lon=df["Longitude"],
        hover_name=df["City"],
        color=df["Price"],
        title="House Price Map",
        mapbox_style="open-street-map",
        size=df["Price_per_Bedroom"],
        zoom=3
    )
    map_fig.update_layout(
        # Customize the style of the plot
        margin = dict(l=30, r=30, t=60, b=60)
    )

    return (
        f"Median Price: ${median_price:,.2f}",
        f"Average Bedrooms: {avg_bedrooms:.2f}",
        f"Price Range: ${min_price:,.2f} - ${max_price:,.2f}",
        chart1, chart2, chart3, map_fig
    )

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
