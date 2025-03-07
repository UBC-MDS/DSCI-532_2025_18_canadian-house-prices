import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, html
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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
         Input("bedrooms-slider", "value")]
    )
    def update_dashboard(selected_cities, selected_provinces, bedrooms_range):
        filtered_df = df.copy()

        if selected_cities:
            filtered_df = filtered_df[filtered_df["City"].isin(selected_cities)]
        if selected_provinces:
            filtered_df = filtered_df[filtered_df["Province"].isin(selected_provinces)]
        if bedrooms_range:
            filtered_df = filtered_df[(filtered_df["Number_Beds"] >= bedrooms_range[0]) & 
                                      (filtered_df["Number_Beds"] <= bedrooms_range[1])]

        median_price = filtered_df["Price"].median()
        avg_bedrooms = filtered_df["Number_Beds"].mean()
        min_price = filtered_df["Price"].min()
        max_price = filtered_df["Price"].max()

        city_price_distribution = px.box(filtered_df, x="City", y="Price", title="City Price Distribution")
        return html.Div(f"${median_price:,.0f}"), html.Div(f"{avg_bedrooms:.2f}"), html.Div(f"${min_price:,.0f} - ${max_price:,.0f}"), city_price_distribution
