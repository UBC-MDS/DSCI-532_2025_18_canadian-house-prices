from dash import Output, Input
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from src.utils.data_loader import load_data

# Load the dataset
df = load_data()

# Define constants for chart styling
CHART_AXIS_TITLE_FONT_SIZE = 18
CHART_AXIS_TICKFONT_FONT_SIZE = 16

def register_callbacks(app):
    """
    Register callbacks with the Dash application to update the dashboard components.
    
    Args:
        app: The Dash application instance.
    """
    @app.callback(
        [Output("median-price", "children"),
         Output("avg-bedrooms", "children"),
         Output("avg-bathrooms", "children"),
         Output("price-range", "children"),
         Output("chart1", "figure"),
         Output("chart2", "figure"),
         Output("chart3", "figure"),
         Output("map", "spec")],  # Changed to "spec" for Altair
        [Input("city-filter", "value"),
         Input("province-filter", "value"),
         Input("bedrooms-slider", "value"),
         Input("bathrooms-slider", "value")]
    )

    def update_dashboard(selected_cities, selected_provinces, bedrooms_range, bathrooms_range):
        """
        Update the dashboard components based on user inputs.
        
        Args:
            selected_cities (list): List of selected city names.
            selected_provinces (list): List of selected province names.
            bedrooms_range (list): Range of bedrooms [min, max].
            bathrooms_range (list): Range of bathrooms [min, max].
        
        Returns:
            tuple: Updated content for summary cards and chart figures.
        """
        # Filter the dataset based on user inputs

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
        avg_bathrooms = filtered_df["Number_Baths"].mean()
        min_price = filtered_df["Price"].min()
        max_price = filtered_df["Price"].max()

        # Chart 1: City Price Distribution (Box Plot)
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

        # Chart 2: Price vs Number of Bedrooms (Box Plot)
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

        # Chart 3: Bubble Chart - Median House Price to Income Ratio by City
        if not filtered_df.empty:
            # Aggregate data by city to get median values
            city_data = filtered_df.groupby("City").agg({
                "Price": "median",            # Median house price
                "Median_Family_Income": "median",  # Median family income
                "Population": "first",         # Population (assuming consistent per city)
                "Province": "first"
            }).reset_index()

            # Calculate the price-to-income ratio
            city_data["Price_Income_Ratio"] = city_data["Price"] / city_data["Median_Family_Income"]

            # Create the bubble chart
            bubble_chart = px.scatter(
                city_data,
                x="City",
                y="Price_Income_Ratio",
                size="Population",
                color="Province",
                hover_name="City",
                hover_data={"Population": True, "Price_Income_Ratio": ":.2f"},
                title="Median House Price to Family Income Ratio by City",
                template="plotly_white",
                size_max = 60
            )

            bubble_chart.update_traces(marker=dict(sizemin=15))

            # Update layout for better appearance
            bubble_chart.update_layout(
                xaxis_title="City",
                yaxis_title="Price to Family Income Ratio",
                xaxis_tickangle=-45,  # Rotate x-axis labels for readability
                title=dict(
                    text="Median House Price to Income Ratio by City",
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
        else:
            # If no data is available, return an empty figure
            bubble_chart = go.Figure()
            bubble_chart.update_layout(
                title="Median House Price to Income Ratio by City",
                xaxis_title="City",
                yaxis_title="Price to Income Ratio",
                template="plotly_white"
            )

        # Define GeoJSON source for Canadian provinces
        geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/canada.geojson"

        # Prepare data for Wikipedia links
        wikipedia_data = pd.DataFrame({
            "name": filtered_df["Province"].unique() if selected_provinces else df["Province"].unique(),
            "wikipedia": [
                f"https://en.wikipedia.org/wiki/{prov.replace(' ', '_')}" for prov in 
                (filtered_df["Province"].unique() if selected_provinces else df["Province"].unique())
            ]
        })

        map_df = filtered_df.groupby("City").agg({
                "Latitude": "mean",
                "Longitude": "mean",
                "Price": "median",
                "Number_Beds": "mean"
            }).reset_index()

        # Hardcode Halifax's coordinates (For Milestone 3 only, will look into it later)
        if "Halifax" in map_df["City"].values:
            map_df.loc[map_df["City"] == "Halifax", "Latitude"] = 44.6488
            map_df.loc[map_df["City"] == "Halifax", "Longitude"] = -63.5752

        # Create the base Altair map (provinces)
        base_map = alt.Chart(
            alt.Data(url=geojson_url, format=alt.DataFormat(property='features'))
        ).mark_geoshape(
            stroke='white'
        ).project(
            'transverseMercator',
            rotate=[90, 0, 0]
        ).encode(
            tooltip=alt.Tooltip('properties.name:N', title="Province"),
            color=alt.Color('properties.name:N', scale=alt.Scale(scheme='tableau20'), legend=None),
            href='wikipedia:N'
        ).transform_lookup(
            lookup='properties.name',
            from_=alt.LookupData(wikipedia_data, 'name', ['wikipedia'])
        )

        # Create city markers layer
        city_markers = alt.Chart(map_df).mark_circle(
            # size=120,
        ).encode(
            longitude='Longitude:Q',
            latitude='Latitude:Q',
            color=alt.Color('Price:Q', scale=alt.Scale(scheme='viridis')),
            size=alt.Size('Price:Q', scale=alt.Scale(range=[50, 500])),
            tooltip=[
                alt.Tooltip('City:N', title="City"),
                alt.Tooltip('Price:Q', title="Median Price", format=",.0f"),
                alt.Tooltip('Number_Beds:Q', title="Average Bedrooms", format=".2f")
            ]
        )

        # Combine base map and city markers
        final_map = (base_map + city_markers).properties(
            width="container",
            height="container",
            title="Map of Canadian Provinces with Selected Cities"
        ).configure_title(
            fontSize=25,
            font='Roboto, sans-serif',
            color="#000000",
            anchor='middle'
        )

        # Return updated content for summary cards and chart figures
        return (
            html.Div([
                html.H5("Median Price", style={"margin": "0", "color": "#FFFFFF"}),
                html.H3(f"${median_price:,.0f}", style={"margin": "0", "color": "#1E88E5"})
            ]),
            html.Div([
                html.H5("Average Bedrooms", style={"margin": "0", "color": "#FFFFFF"}),
                html.H3(f"{avg_bedrooms:.2f}", style={"margin": "0", "color": "#1E88E5"})
            ]),
            html.Div([ 
                html.H5("Average Bathrooms", style={"margin": "0", "color": "#FFFFFF"}),
                html.H3(f"{avg_bathrooms:.2f}", style={"margin": "0", "color": "#1E88E5"})
            ]),
            html.Div([
                html.H5("Price Range", style={"margin": "0", "color": "#FFFFFF"}),
                html.H3(f"${min_price:,.0f} - ${max_price:,.0f}", style={"margin": "0", "color": "#1E88E5"})
            ]),
            city_price_distribution,
            price_vs_bedrooms,
            bubble_chart,
            final_map.to_dict()  # Output Altair chart spec with city markers
        )
