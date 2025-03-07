from dash import Output, Input
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.utils.data_loader import load_data

df = load_data()

CHART_AXIS_TITLE_FONT_SIZE = 18
CHART_AXIS_TICKFONT_FONT_SIZE = 16

def register_callbacks(app):
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
        # Apply filtering logic based on user inputs
        filtered_df = df.copy()

        if selected_cities:
            filtered_df = filtered_df[filtered_df["City"].isin(selected_cities)]
        if selected_provinces:
            filtered_df = filtered_df[filtered_df["Province"].isin(selected_provinces)]
        if bedrooms_range:
            filtered_df = filtered_df[(filtered_df["Number_Beds"] >= bedrooms_range[0]) & 
                                      (filtered_df["Number_Beds"] <= bedrooms_range[1])]
        if bathrooms_range:
            filtered_df = filtered_df[(filtered_df["Number_Baths"] >= bathrooms_range[0]) & 
                                      (filtered_df["Number_Baths"] <= bathrooms_range[1])]

        # Calculate summary statistics
        median_price = filtered_df["Price"].median()
        avg_bedrooms = filtered_df["Number_Beds"].mean()
        min_price = filtered_df["Price"].min()
        max_price = filtered_df["Price"].max()

        # City Price Distribution (Box Plot)
        city_price_distribution = px.box(
            filtered_df,
            x="City",
            y="Price",
            title="City Price Distribution",
            template="plotly_white"
        )
        city_price_distribution.update_layout(
            title=dict(
                text="City Price Distribution",
                font=dict(size=25, family="Roboto, sans-serif", color="#000000"),
                x=0.5,
                y=0.95,
                xanchor="center",
                yanchor="top"
            ),
            xaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,
            yaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,
            xaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,
            yaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,
            plot_bgcolor="#F5F5F5",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=50, b=10)
        )

        # Price vs Number of Bedrooms (Box Plot)
        price_vs_bedrooms = px.box(
            filtered_df,
            x="Number_Beds",
            y="Price",
            title="Price vs Number of Bedrooms",
            labels={"Number_Beds": "Number of Bedrooms"},
            template="plotly_white"
        )
        price_vs_bedrooms.update_layout(
            title=dict(
                text="Price vs Number of Bedrooms",
                font=dict(size=25, family="Roboto, sans-serif", color="#000000"),
                x=0.5,
                y=0.95,
                xanchor="center",
                yanchor="top"
            ),
            xaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,
            yaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,
            xaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,
            yaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,
            plot_bgcolor="#F5F5F5",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=50, b=10)
        )

        # Median Price Across Cities (Bar Chart)
        city_median_price = filtered_df.groupby("City")["Price"].median().sort_values()
        median_price_comparison = go.Figure(
            data=[go.Bar(
                x=city_median_price.index,
                y=city_median_price.values,
                marker=dict(color="#1E88E5")
            )],
            layout=go.Layout(
                title=dict(
                    text="Median Price Across Cities",
                    font=dict(size=25, family="Roboto, sans-serif", color="#000000"),
                    x=0.5,
                    y=0.95,
                    xanchor="center",
                    yanchor="top"
                ),
                xaxis=dict(title="City"),
                yaxis=dict(title="Median Price (CAD)"),
                template="plotly_white",
                plot_bgcolor="#F5F5F5",
                paper_bgcolor="#FFFFFF",
                xaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,
                yaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,
                xaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,
                yaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,
                margin=dict(l=10, r=10, t=50, b=10)
            )
        )

        # Geospatial Price Distribution (Interactive Map)
        if selected_cities:
            map_df = filtered_df[filtered_df["City"].isin(selected_cities)].groupby("City").agg({
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
                hover_name="City",
                hover_data={"Price": ":,.0f", "Number_Beds": ":,.0f"},
                title="Geospatial Price Distribution",
                mapbox_style="carto-positron",
                center={"lat": 55.0, "lon": -95.0},
                zoom=2,
            )
        else:
            geospatial_price_distribution = go.Figure(go.Scattermapbox())
            geospatial_price_distribution.update_layout(
                mapbox_style="carto-positron",
                mapbox_center={"lat": 55.0, "lon": -95.0},
                mapbox_zoom=2,
                title="Geospatial Price Distribution",
                title_x=0.5
            )

        geospatial_price_distribution.update_layout(
            title=dict(
                text="Geospatial Price Distribution",
                font=dict(size=25, family="Roboto, sans-serif", color="#000000"),
                x=0.5,
                y=0.95,
                xanchor="center",
                yanchor="top"
            ),
            plot_bgcolor="#F5F5F5",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=50, b=10),
            mapbox={
                "layers": [{
                    "sourcetype": "geojson",
                    "source": "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/canada.geojson",
                    "type": "line",
                    "color": "pink",
                    "line": {"width": 1}
                }]
            }
        )

        # Return all outputs
        return (
            html.Div([
                html.H5("Median Price", style={"margin": "0"}),
                html.H3(f"${median_price:,.0f}", style={"margin": "0", "color": "#1E88E5"})
            ]),
            html.Div([
                html.H5("Average Bedrooms", style={"margin": "0"}),
                html.H3(f"{avg_bedrooms:.2f}", style={"margin": "0", "color": "#1E88E5"})
            ]),
            html.Div([
                html.H5("Price Range", style={"margin": "0"}),
                html.H3(f"${min_price:,.0f} - ${max_price:,.0f}", style={"margin": "0", "color": "#1E88E5"})
            ]),
            city_price_distribution,
            price_vs_bedrooms,
            median_price_comparison,
            geospatial_price_distribution
        )