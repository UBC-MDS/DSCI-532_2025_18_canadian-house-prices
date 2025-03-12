from dash import Output, Input
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from src.utils.data_loader import load_data
import requests  # For fetching GeoJSON data

# Load the dataset
df = load_data()

# Define constants for chart styling
CHART_AXIS_TITLE_FONT_SIZE = 18
CHART_AXIS_TICKFONT_FONT_SIZE = 16

# Enable vegafusion for better Altair performance with large datasets
alt.data_transformers.enable("vegafusion")

def register_callbacks(app):
    @app.callback(
        [Output("median-price", "children"),
         Output("avg-bedrooms", "children"),
         Output("avg-bathrooms", "children"),
         Output("price-range", "children"),
         Output("chart1", "spec"),
         Output("chart2", "spec"),
         Output("chart3", "figure"),
         Output("map", "spec")],
        [Input("city-filter", "value"),
         Input("province-filter", "value"),
         Input("bedrooms-slider", "value"),
         Input("bathrooms-slider", "value")]
    )
    def update_dashboard(selected_cities, selected_provinces, bedrooms_range, bathrooms_range):
        # Create a copy of the dataframe to filter
        filtered_df = df.copy()
        
        # Apply filters based on user inputs
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

        # Function to compute boxplot statistics for a given group
        def compute_boxplot_stats(group_df, group_col):
            stats = group_df.groupby(group_col)["Price"].describe().reset_index()
            stats = stats.rename(columns={'25%': 'Q1', '50%': 'median', '75%': 'Q3'})
            stats['IQR'] = stats['Q3'] - stats['Q1']
            stats['whisker_low_limit'] = stats['Q1'] - 1.5 * stats['IQR']
            stats['whisker_high_limit'] = stats['Q3'] + 1.5 * stats['IQR']

            # Compute actual whisker ends (Min and Max within whiskers)
            def get_whiskers(group):
                q1 = group['Price'].quantile(0.25)
                q3 = group['Price'].quantile(0.75)
                iqr = q3 - q1
                whisker_low_limit = q1 - 1.5 * iqr
                whisker_high_limit = q3 + 1.5 * iqr
                whisker_low = group['Price'][group['Price'] >= whisker_low_limit].min()
                whisker_high = group['Price'][group['Price'] <= whisker_high_limit].max()
                return pd.Series({'Min': whisker_low, 'Max': whisker_high})

            whiskers = group_df.groupby(group_col).apply(get_whiskers).reset_index()
            stats = stats.merge(whiskers, on=group_col)

            # Identify outliers in the original data
            stats_subset = stats[[group_col, 'Min', 'Max']]
            group_df = group_df.merge(stats_subset, on=group_col, how="left")
            group_df['is_outlier'] = (group_df['Price'] < group_df['Min']) | (group_df['Price'] > group_df['Max'])
            return stats, group_df

        # Chart 1: City Price Distribution (Altair Boxplot)
        if not filtered_df.empty:
            stats_city, outliers_city = compute_boxplot_stats(filtered_df, "City")

            # Compute the sorted order based on median price
            city_medians = filtered_df.groupby("City")["Price"].median().sort_values()
            sorted_cities = city_medians.index.tolist()

            # Define the x-encoding with sorting by median price
            x_encoding_city = alt.X("City:N", scale=alt.Scale(paddingInner=0.5), title="City", sort=sorted_cities)

            # Boxes (Q1 to Q3)
            box_city = alt.Chart(stats_city).mark_bar().encode(
                x=x_encoding_city,
                y=alt.Y("Q1:Q", title="Price"),
                y2="Q3:Q",
                color="City:N",
                tooltip=[
                    alt.Tooltip("City:N", title="City"),
                    alt.Tooltip("Max:Q", title="Max", format="$,.0f"),
                    alt.Tooltip("Q3:Q", title="Q3", format="$,.0f"),
                    alt.Tooltip("median:Q", title="Median", format="$,.0f"),
                    alt.Tooltip("Q1:Q", title="Q1", format="$,.0f"),
                    alt.Tooltip("Min:Q", title="Min", format="$,.0f")
                ]
            )

            # Median line
            median_city = alt.Chart(stats_city).mark_tick(color="white", size=20).encode(
                x=x_encoding_city,
                y="median:Q",
                tooltip=[
                    alt.Tooltip("City:N", title="City"),
                    alt.Tooltip("Max:Q", title="Max", format="$,.0f"),
                    alt.Tooltip("Q3:Q", title="Q3", format="$,.0f"),
                    alt.Tooltip("median:Q", title="Median", format="$,.0f"),
                    alt.Tooltip("Q1:Q", title="Q1", format="$,.0f"),
                    alt.Tooltip("Min:Q", title="Min", format="$,.0f")
                ]
            )

            # Whiskers (low and high)
            whiskers_city = (
                alt.Chart(stats_city).mark_rule().encode(
                    x=x_encoding_city,
                    y="Min:Q",
                    y2="Q1:Q",
                    color="City:N",
                    tooltip=[
                        alt.Tooltip("City:N", title="City"),
                        alt.Tooltip("Min:Q", title="Min", format="$,.0f")
                    ]
                ) + alt.Chart(stats_city).mark_rule().encode(
                    x=x_encoding_city,
                    y="Q3:Q",
                    y2="Max:Q",
                    color="City:N",
                    tooltip=[
                        alt.Tooltip("City:N", title="City"),
                        alt.Tooltip("Max:Q", title="Max", format="$,.0f")
                    ]
                )
            )

            # Outliers
            outliers_plot_city = alt.Chart(outliers_city[outliers_city["is_outlier"]]).mark_point().encode(
                x=x_encoding_city,
                y="Price:Q",
                color="City:N",
                tooltip=[
                    alt.Tooltip("City:N", title="City"),
                    alt.Tooltip("Price:Q", title="Price", format="$,.0f")
                ]
            )

            # Combine all layers for Chart 1
            chart1 = (whiskers_city + box_city + median_city + outliers_plot_city).properties(
                width="container",
                height="container",
                title="City Price Distribution (Sorted by Median Price)"
            ).configure_title(
                fontSize=25,
                font="Roboto, sans-serif",
                color="#000000",
                anchor="middle"
            ).configure_axis(
                labelFontSize=CHART_AXIS_TICKFONT_FONT_SIZE,
                titleFontSize=CHART_AXIS_TITLE_FONT_SIZE
            ).configure_view(
                strokeWidth=0
            )
            chart1_spec = chart1.to_dict(format="vega")
            chart1_spec["autosize"] = {"type": "fit", "contains": "padding"}
        else:
            chart1_spec = alt.Chart(pd.DataFrame()).mark_text().encode(
                text=alt.value("No Data Available")
            ).properties(
                title="City Price Distribution (Sorted by Median Price)",
                width=600,
                height=400
            ).configure_title(
                fontSize=25,
                font="Roboto, sans-serif",
                color="#000000",
                anchor="middle"
            ).to_dict()

        # Chart 2: Price vs Number of Bedrooms (Altair Boxplot)
        if not filtered_df.empty:
            stats_bedrooms, outliers_bedrooms = compute_boxplot_stats(filtered_df, "Number_Beds")

            # Define the x-encoding with increased padding to narrow the boxes
            x_encoding_bedrooms = alt.X("Number_Beds:N", scale=alt.Scale(paddingInner=0.5), title="Number of Bedrooms")

            # Boxes (Q1 to Q3)
            box_bedrooms = alt.Chart(stats_bedrooms).mark_bar().encode(
                x=x_encoding_bedrooms,
                y=alt.Y("Q1:Q", title="Price"),
                y2="Q3:Q",
                color="Number_Beds:N",
                tooltip=[
                    alt.Tooltip("Number_Beds:N", title="Number of Bedrooms"),
                    alt.Tooltip("Max:Q", title="Max", format="$,.0f"),
                    alt.Tooltip("Q3:Q", title="Q3", format="$,.0f"),
                    alt.Tooltip("median:Q", title="Median", format="$,.0f"),
                    alt.Tooltip("Q1:Q", title="Q1", format="$,.0f"),
                    alt.Tooltip("Min:Q", title="Min", format="$,.0f")
                ]
            )

            # Median line
            median_bedrooms = alt.Chart(stats_bedrooms).mark_tick(color="white", size=20).encode(
                x=x_encoding_bedrooms,
                y="median:Q",
                tooltip=[
                    alt.Tooltip("Number_Beds:N", title="Number of Bedrooms"),
                    alt.Tooltip("Max:Q", title="Max", format="$,.0f"),
                    alt.Tooltip("Q3:Q", title="Q3", format="$,.0f"),
                    alt.Tooltip("median:Q", title="Median", format="$,.0f"),
                    alt.Tooltip("Q1:Q", title="Q1", format="$,.0f"),
                    alt.Tooltip("Min:Q", title="Min", format="$,.0f")
                ]
            )

            # Whiskers (low and high)
            whiskers_bedrooms = (
                alt.Chart(stats_bedrooms).mark_rule().encode(
                    x=x_encoding_bedrooms,
                    y="Min:Q",
                    y2="Q1:Q",
                    color="Number_Beds:N",
                    tooltip=[
                        alt.Tooltip("Number_Beds:N", title="Number of Bedrooms"),
                        alt.Tooltip("Min:Q", title="Min", format="$,.0f")
                    ]
                ) + alt.Chart(stats_bedrooms).mark_rule().encode(
                    x=x_encoding_bedrooms,
                    y="Q3:Q",
                    y2="Max:Q",
                    color="Number_Beds:N",
                    tooltip=[
                        alt.Tooltip("Number_Beds:N", title="Number of Bedrooms"),
                        alt.Tooltip("Max:Q", title="Max", format="$,.0f")
                    ]
                )
            )

            # Outliers
            outliers_plot_bedrooms = alt.Chart(outliers_bedrooms[outliers_bedrooms["is_outlier"]]).mark_point().encode(
                x=x_encoding_bedrooms,
                y="Price:Q",
                color="Number_Beds:N",
                tooltip=[
                    alt.Tooltip("Number_Beds:N", title="Number of Bedrooms"),
                    alt.Tooltip("Price:Q", title="Price", format="$,.0f")
                ]
            )

            # Combine all layers for Chart 2
            chart2 = (whiskers_bedrooms + box_bedrooms + median_bedrooms + outliers_plot_bedrooms).properties(
                width="container",
                height="container",
                title="Price vs Number of Bedrooms"
            ).configure_title(
                fontSize=25,
                font="Roboto, sans-serif",
                color="#000000",
                anchor="middle"
            ).configure_axis(
                labelFontSize=CHART_AXIS_TICKFONT_FONT_SIZE,
                titleFontSize=CHART_AXIS_TITLE_FONT_SIZE
            ).configure_view(
                strokeWidth=0
            )
            chart2_spec = chart2.to_dict(format="vega")
            chart2_spec["autosize"] = {"type": "fit", "contains": "padding"}
        else:
            chart2_spec = alt.Chart(pd.DataFrame()).mark_text().encode(
                text=alt.value("No Data Available")
            ).properties(
                title="Price vs Number of Bedrooms",
                width=600,
                height=400
            ).configure_title(
                fontSize=25,
                font="Roboto, sans-serif",
                color="#000000",
                anchor="middle"
            ).to_dict()

        # Chart 3: Bubble Chart - Median House Price to Income Ratio by City (Plotly)
        if not filtered_df.empty:
            city_data = filtered_df.groupby("City").agg({
                "Price": "median",
                "Median_Family_Income": "median",
                "Population": "first",
                "Province": "first"
            }).reset_index()
            city_data["Price_Income_Ratio"] = city_data["Price"] / city_data["Median_Family_Income"]

            bubble_chart = px.scatter(
                city_data,
                x="City",
                y="Price_Income_Ratio",
                size="Population",
                color="Province",
                hover_name="City",
                custom_data=["Price", "Province"],
                title="Median House Price to Family Income Ratio by City",
                template="plotly_white",
                size_max=60
            )
            bubble_chart.update_traces(
                marker=dict(sizemin=15),
                hovertemplate=(
                    "<b>%{hovertext}</b><br>" +
                    "Province: %{customdata[1]}<br>" +
                    "Population: %{marker.size:,.0f}<br>" +
                    "Median Price: %{customdata[0]:$,.0f}<br>" +
                    "Price-Income Ratio: %{y:.2f}<extra></extra>"
                )
            )
            bubble_chart.update_layout(
                xaxis_title="City",
                yaxis_title="Price to Family Income Ratio",
                xaxis_tickangle=-45,
                title=dict(
                    text="Median House Price to Family Income Ratio by City",
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
            bubble_chart = go.Figure()
            bubble_chart.update_layout(
                title="Median House Price to Family Income Ratio by City",
                xaxis_title="City",
                yaxis_title="Price to Income Ratio",
                template="plotly_white"
            )

        # Map: Altair-based map of Canadian provinces with city markers
        geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/canada.geojson"
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

        # Adjust Halifax coordinates if present
        if "Halifax" in map_df["City"].values:
            map_df.loc[map_df["City"] == "Halifax", "Latitude"] = 44.6488
            map_df.loc[map_df["City"] == "Halifax", "Longitude"] = -63.5752

        # Fetch GeoJSON data
        try:
            response = requests.get(geojson_url)
            response.raise_for_status()  # Raise an error if the request fails
            geojson_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching GeoJSON: {e}")
            geojson_data = {"features": []}  # Fallback to empty data

        base_map = alt.Chart(
            alt.Data(values=geojson_data['features'])
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

        city_markers = alt.Chart(map_df).mark_circle().encode(
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

        # Return updated content
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
            chart1_spec,
            chart2_spec,
            bubble_chart,
            final_map.to_dict(format="vega")
        )