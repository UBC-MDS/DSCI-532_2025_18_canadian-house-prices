import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
import pandas as pd
import plotly.express as px

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
            dbc.CardBody(dcc.Graph(id="chart1", style={"height": "250px"}))
        ]), width=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Placeholder Chart 2"),
            dbc.CardBody(dcc.Graph(id="chart2", style={"height": "250px"}))
        ]), width=6)
    ], className="mb-2"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Placeholder Chart 3"),
            dbc.CardBody(dcc.Graph(id="chart3", style={"height": "250px"}))
        ]), width=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Map"),
            dbc.CardBody(dcc.Graph(id="map", style={"height": "250px"}))
        ]), width=6)
    ], className="mb-2")

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
    chart2 = px.box(x=["X", "Y", "Z"], y=[5, 15, 10], title="Chart 2")
    chart3 = px.scatter(x=["D", "E", "F"], y=[12, 9, 14], title="Chart 3")

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

    return (
        f"Median Price: ${median_price:,.2f}",
        f"Average Bedrooms: {avg_bedrooms:.2f}",
        f"Price Range: ${min_price:,.2f} - ${max_price:,.2f}",
        chart1, chart2, chart3, map_fig
    )

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
