import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, html
from utils.data_loader import load_data

df = load_data()

def register_chart_callbacks(app):
    @app.callback(
        [Output("median-price", "children"),
         Output("avg-bedrooms", "children"),
         Output("price-range", "children"),
         Output("chart1", "figure"),
         Output("chart2", "figure"),
         Output("chart3", "figure"),
         Output("map", "figure")],
        [Input("city-filter", "value"),
         Input("province-filter", "value"),
         Input("bedrooms-slider", "value"),
         Input("bathrooms-slider", "value")]
    )
    def update_dashboard(selected_cities, selected_provinces, bedrooms_range, bathrooms_range):
        # Apply filtering logic
        filtered_df = df.copy()

        if selected_cities:
            filtered_df = filtered_df[filtered_df["City"].isin(selected_cities)]
        if selected_provinces:
            filtered_df = filtered_df[filtered_df["Province"].isin(selected_provinces)]
        if bedrooms_range:
            filtered_df = filtered_df[
                (filtered_df["Number_Beds"] >= bedrooms_range[0]) & 
                (filtered_df["Number_Beds"] <= bedrooms_range[1])
            ]
        if bathrooms_range:
            filtered_df = filtered_df[
                (filtered_df["Number_Baths"] >= bathrooms_range[0]) & 
                (filtered_df["Number_Baths"] <= bathrooms_range[1])
            ]

        # Calculate summary stats
        median_price = filtered_df["Price"].median() if not filtered_df.empty else 0
        avg_bedrooms = filtered_df["Number_Beds"].mean() if not filtered_df.empty else 0
        min_price = filtered_df["Price"].min() if not filtered_df.empty else 0
        max_price = filtered_df["Price"].max() if not filtered_df.empty else 0

        # Ensure charts are created even if no data is available
        if filtered_df.empty:
            city_price_distribution = go.Figure()
            price_vs_bedrooms = go.Figure()
            median_price_comparison = go.Figure()
            geospatial_price_distribution = go.Figure()
        else:
            city_price_distribution = px.box(filtered_df, x="City", y="Price", title="City Price Distribution")
            price_vs_bedrooms = px.box(filtered_df, x="Number_Beds", y="Price", title="Price vs Number of Bedrooms")
            median_price_comparison = go.Figure(data=[go.Bar(
                x=filtered_df["City"].unique(),
                y=filtered_df.groupby("City")["Price"].median(),
                marker=dict(color="#1E88E5")
            )])

            if selected_cities:
                map_df = filtered_df.groupby("City").agg({
                    "Latitude": "mean",
                    "Longitude": "mean",
                    "Price": "median",
                    "Number_Beds": "mean"
                }).reset_index()
            else:
                map_df = pd.DataFrame()

            if not map_df.empty:
                geospatial_price_distribution = px.scatter_mapbox(
                    map_df,
                    lat="Latitude",
                    lon="Longitude",
                    color="Price",
                    size="Price",
                    title="Geospatial Price Distribution",
                    mapbox_style="carto-positron",
                    zoom=2
                )
            else:
                geospatial_price_distribution = go.Figure()

        # Ensure the function always returns 7 values
        return (
            html.Div(f"${median_price:,.0f}"),
            html.Div(f"{avg_bedrooms:.2f}"),
            html.Div(f"${min_price:,.0f} - ${max_price:,.0f}"),
            city_price_distribution,
            price_vs_bedrooms,
            median_price_comparison,
            geospatial_price_distribution
        )
