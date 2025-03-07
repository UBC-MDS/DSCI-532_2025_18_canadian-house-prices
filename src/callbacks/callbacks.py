from dash import Input, Output
import plotly.express as px
from app import app
from utils.data_loader import load_data

df = load_data()

@app.callback(
    [
        Output("median-price", "children"),
        Output("avg-bedrooms", "children"),
        Output("price-range", "children"),
        Output("chart1", "figure"),
        Output("chart2", "figure"),
        Output("chart3", "figure"),
        Output("map-figure", "figure")
    ],
    [
        Input("city-filter", "value"),
        Input("province-filter", "value"),
        Input("bedrooms-slider", "value"),
        Input("bathrooms-slider", "value")
    ]
)
def update_dashboard(cities, provinces, bedrooms_range, bathrooms_range):
    filtered_df = df.copy()
    if cities:
        filtered_df = filtered_df[filtered_df["City"].isin(cities)]
    if provinces:
        filtered_df = filtered_df[filtered_df["Province"].isin(provinces)]
    filtered_df = filtered_df[
        (filtered_df["Number_Beds"].between(*bedrooms_range)) &
        (filtered_df["Number_Baths"].between(*bathrooms_range))
    ]

    median_price = filtered_df["Price"].median()
    avg_bedrooms = filtered_df["Number_Beds"].mean()
    min_price = filtered_df["Price"].min()
    max_price = filtered_df["Price"].max()

    city_price_distribution = px.box(filtered_df, x="City", y="Price", title="City Price Distribution")
    price_vs_bedrooms = px.box(filtered_df, x="Number_Beds", y="Price", title="Price vs Bedrooms")
    median_price_comparison = px.bar(
        filtered_df.groupby("City", as_index=False)["Price"].median(),
        x="City",
        y="Price",
        title="Median Price by City"
    )

    map_df = filtered_df.groupby("City").agg({"Latitude": "mean", "Longitude": "mean", "Price": "median"}).reset_index()
    geospatial_price_distribution = px.scatter_mapbox(
        map_df, lat="Latitude", lon="Longitude",
        size="Price", color="Price",
        zoom=3, mapbox_style="carto-positron"
    )

    return (
        f"${median_price:,.0f}",
        f"{avg_bedrooms:.2f}",
        f"${min_price:,.0f} - ${max_price:,.0f}",
        city_price_distribution,
        price_vs_bedrooms,
        median_price_comparison,
        geospatial_price_distribution
    )

@app.callback(
    Output("city-filter", "options"),
    Input("province-filter", "value")
)
def update_city_options(selected_provinces):
    if selected_provinces:
        filtered_df = df[df["Province"].isin(selected_provinces)]
        return [{"label": city, "value": city} for city in filtered_df["City"].unique()]
    return [{"label": city, "value": city} for city in df["City"].unique()]

@app.callback(
    [
        Output("city-filter", "value"),
        Output("province-filter", "value"),
        Output("bedrooms-slider", "value"),
        Output("bathrooms-slider", "value")
    ],
    Input("reset-button", "n_clicks"),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    return (
        ["Vancouver", "Toronto", "Montreal", "Ottawa"],
        [],
        [df["Number_Beds"].min(), df["Number_Beds"].max()],
        [df["Number_Baths"].min(), df["Number_Baths"].max()]
    )
