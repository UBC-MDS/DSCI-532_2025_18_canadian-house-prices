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

        # Ensure function always returns 7 outputs
        if filtered_df.empty:
            return (
                html.Div("No Data", style={"color": "red"}),
                html.Div("No Data", style={"color": "red"}),
                html.Div("No Data", style={"color": "red"}),
                go.Figure(),
                go.Figure(),
                go.Figure(),
                go.Figure()
            )

        # Calculate statistics
        median_price = f"${filtered_df['Price'].median():,.0f}"
        avg_bedrooms = f"{filtered_df['Number_Beds'].mean():.2f}"
        price_range = f"${filtered_df['Price'].min():,.0f} - ${filtered_df['Price'].max():,.0f}"

        # Create figures
        city_price_distribution = px.box(filtered_df, x="City", y="Price", title="City Price Distribution")
        price_vs_bedrooms = px.box(filtered_df, x="Number_Beds", y="Price", title="Price vs Number of Bedrooms")
        median_price_comparison = go.Figure(data=[go.Bar(
            x=filtered_df["City"].unique(),
            y=filtered_df.groupby("City")["Price"].median(),
            marker=dict(color="#1E88E5")
        )])

        geospatial_price_distribution = go.Figure()

        return (
            html.Div(median_price),
            html.Div(avg_bedrooms),
            html.Div(price_range),
            city_price_distribution,
            price_vs_bedrooms,
            median_price_comparison,
            geospatial_price_distribution
        )
