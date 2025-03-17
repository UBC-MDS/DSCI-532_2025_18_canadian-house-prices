from dash import Output, Input
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from src.utils.data_loader import load_data
import requests  # For fetching GeoJSON data
from functools import lru_cache


# Load datasets once when the module is imported
df_locations, df_housing = load_data()

# Define constants for chart styling
CHART_AXIS_TITLE_FONT_SIZE = 18
CHART_AXIS_TICKFONT_FONT_SIZE = 16

# Enable vegafusion for better Altair performance with large datasets
alt.data_transformers.enable("vegafusion")

# Fetch GeoJSON data
geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/canada.geojson"
try:
    response = requests.get(geojson_url)
    response.raise_for_status()
    geojson_data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching GeoJSON: {e}")
    geojson_data = {"features": []}  # Fallback to empty data

@lru_cache(maxsize=1024)
def get_filtered_data(selected_cities: tuple, selected_provinces: tuple, 
                      bedrooms_range: tuple, bathrooms_range: tuple):
    """
    Filter the global df_housing DataFrame based on the provided parameters.

    Args:
        selected_cities: Tuple of selected cities.
        selected_provinces: Tuple of selected provinces.
        bedrooms_range: Tuple of (min, max) bedrooms.
        bathrooms_range: Tuple of (min, max) bathrooms.

    Returns:
        Filtered DataFrame.
    """
    filtered_df = df_housing.copy()
    if selected_cities:
        filtered_df = filtered_df[filtered_df["City"].isin(selected_cities)]
    if selected_provinces:
        filtered_df = filtered_df[filtered_df["Province"].isin(selected_provinces)]
    filtered_df = filtered_df[(filtered_df["Number_Beds"] >= bedrooms_range[0]) & 
                              (filtered_df["Number_Beds"] <= bedrooms_range[1])]
    filtered_df = filtered_df[(filtered_df["Number_Baths"] >= bathrooms_range[0]) & 
                              (filtered_df["Number_Baths"] <= bathrooms_range[1])]
    return filtered_df

def compute_boxplot_stats(group_df, group_col):
    """
    Compute boxplot statistics (quartiles, whiskers, outliers) for a grouped column.
    
    Args:
        group_df: DataFrame to compute statistics on.
        group_col: Column name to group by.
    
    Returns:
        Tuple of (stats DataFrame, DataFrame with outlier flags).
    """
    stats = group_df.groupby(group_col)["Price"].describe().reset_index()
    stats = stats.rename(columns={'25%': 'Q1', '50%': 'median', '75%': 'Q3'})
    stats['IQR'] = stats['Q3'] - stats['Q1']
    stats['whisker_low_limit'] = stats['Q1'] - 1.5 * stats['IQR']
    stats['whisker_high_limit'] = stats['Q3'] + 1.5 * stats['IQR']

    group_df = group_df.merge(stats[[group_col, 'whisker_low_limit', 'whisker_high_limit']], 
                             on=group_col, how='left')
    whisker_low = group_df[group_df['Price'] >= group_df['whisker_low_limit']]\
                     .groupby(group_col)['Price'].min().rename('Min')
    whisker_high = group_df[group_df['Price'] <= group_df['whisker_high_limit']]\
                      .groupby(group_col)['Price'].max().rename('Max')
    stats = stats.merge(whisker_low, on=group_col, how='left')
    stats = stats.merge(whisker_high, on=group_col, how='left')
    group_df['is_outlier'] = (group_df['Price'] < group_df['whisker_low_limit']) | \
                             (group_df['Price'] > group_df['whisker_high_limit'])
    return stats, group_df

def register_callbacks(app):
    """
    Register callbacks for the Dash application to update the dashboard
    based on user inputs.
    
    Args:
        app: The Dash application instance.
    """
    # Callback 1: Update filtered data store
    @app.callback(
        Output('filtered-data', 'data'),
        [Input('city-filter', 'value'),
         Input('province-filter', 'value'),
         Input('bedrooms-slider', 'value'),
         Input('bathrooms-slider', 'value')]
    )
    def update_filtered_data(selected_cities, selected_provinces, bedrooms_range, bathrooms_range):
        selected_cities_tuple = tuple(selected_cities) if selected_cities else tuple()
        selected_provinces_tuple = tuple(selected_provinces) if selected_provinces else tuple()
        bedrooms_range_tuple = tuple(bedrooms_range)
        bathrooms_range_tuple = tuple(bathrooms_range)
        filtered_df = get_filtered_data(selected_cities_tuple, selected_provinces_tuple, 
                                        bedrooms_range_tuple, bathrooms_range_tuple)
        return filtered_df.to_dict('records')

    # Callback 2: Update summary statistics
    @app.callback(
        [Output("median-price", "children"),
         Output("avg-bedrooms", "children"),
         Output("avg-bathrooms", "children"),
         Output("price-range", "children")],
        Input('filtered-data', 'data')
    )
    def update_summary_stats(data):
        if not data:
            return ["N/A", "N/A", "N/A", "N/A"]
        df = pd.DataFrame(data)
        median_price = df["Price"].median()
        avg_bedrooms = df["Number_Beds"].mean()
        avg_bathrooms = df["Number_Baths"].mean()
        min_price = df["Price"].min()
        max_price = df["Price"].max()
        return [
            html.Div([html.H5("Median Price", style={"margin": "0", "color": "#FFFFFF"}), 
                      html.H3(f"${median_price:,.0f}", style={"margin": "0", "color": "#1E88E5"})]),
            html.Div([html.H5("Average Bedrooms", style={"margin": "0", "color": "#FFFFFF"}), 
                      html.H3(f"{avg_bedrooms:.2f}", style={"margin": "0", "color": "#1E88E5"})]),
            html.Div([html.H5("Average Bathrooms", style={"margin": "0", "color": "#FFFFFF"}), 
                      html.H3(f"{avg_bathrooms:.2f}", style={"margin": "0", "color": "#1E88E5"})]),
            html.Div([html.H5("Price Range", style={"margin": "0", "color": "#FFFFFF"}), 
                      html.H3(f"${min_price:,.0f} - ${max_price:,.0f}", style={"margin": "0", "color": "#1E88E5"})])
        ]

    # Callback 3: Update Chart 1 (City Price Distribution)
    @app.callback(
        Output("chart1", "spec"),
        Input('filtered-data', 'data')
    )
    def update_chart1(data):
        if not data:
            return alt.Chart(pd.DataFrame()).mark_text().encode(
                text=alt.value("No Data Available")
            ).properties(
                title="City Price Distribution", width=600, height=400
            ).to_dict()
        df = pd.DataFrame(data)
        stats_city, outliers_city = compute_boxplot_stats(df, "City")
        city_medians = df.groupby("City")["Price"].median().sort_values()
        sorted_cities = city_medians.index.tolist()
        x_encoding = alt.X("City:N", scale=alt.Scale(paddingInner=0.5), title="City", sort=sorted_cities)
        box = alt.Chart(stats_city).mark_bar().encode(
            x=x_encoding, y=alt.Y("Q1:Q", title="Price"), y2="Q3:Q", color="City:N",
            tooltip=["City:N", alt.Tooltip("Max:Q", format="$,.0f"), alt.Tooltip("Q3:Q", format="$,.0f"),
                     alt.Tooltip("median:Q", format="$,.0f"), alt.Tooltip("Q1:Q", format="$,.0f"),
                     alt.Tooltip("Min:Q", format="$,.0f")]
        )
        median = alt.Chart(stats_city).mark_tick(color="white", size=20).encode(
            x=x_encoding, y="median:Q",
            tooltip=["City:N", alt.Tooltip("Max:Q", format="$,.0f"), alt.Tooltip("Q3:Q", format="$,.0f"),
                     alt.Tooltip("median:Q", format="$,.0f"), alt.Tooltip("Q1:Q", format="$,.0f"),
                     alt.Tooltip("Min:Q", format="$,.0f")]
        )
        whiskers = (
            alt.Chart(stats_city).mark_rule().encode(x=x_encoding, y="Min:Q", y2="Q1:Q", color="City:N",
                                                     tooltip=["City:N", alt.Tooltip("Min:Q", format="$,.0f")]) +
            alt.Chart(stats_city).mark_rule().encode(x=x_encoding, y="Q3:Q", y2="Max:Q", color="City:N",
                                                     tooltip=["City:N", alt.Tooltip("Max:Q", format="$,.0f")])
        )
        outliers = alt.Chart(outliers_city[outliers_city["is_outlier"]]).mark_point().encode(
            x=x_encoding, y="Price:Q", color="City:N",
            tooltip=["City:N", alt.Tooltip("Price:Q", format="$,.0f")]
        )
        chart = (whiskers + box + median + outliers).properties(
            width="container", height="container", title="City Price Distribution (Sorted by Median Price)"
        ).configure_title(fontSize=25, font="Roboto, sans-serif", color="#000000", anchor="middle"
        ).configure_axis(labelFontSize=CHART_AXIS_TICKFONT_FONT_SIZE, titleFontSize=CHART_AXIS_TITLE_FONT_SIZE
        ).configure_view(strokeWidth=0)
        chart_spec = chart.to_dict(format="vega")
        chart_spec["autosize"] = {"type": "fit", "contains": "padding"}
        return chart_spec

    # Callback 4: Update Chart 2 (Price vs Number of Bedrooms)
    @app.callback(
        Output("chart2", "spec"),
        Input('filtered-data', 'data')
    )
    def update_chart2(data):
        if not data:
            return alt.Chart(pd.DataFrame()).mark_text().encode(
                text=alt.value("No Data Available")
            ).properties(
                title="Price vs Number of Bedrooms", width=600, height=400
            ).to_dict()
        df = pd.DataFrame(data)
        stats_bedrooms, outliers_bedrooms = compute_boxplot_stats(df, "Number_Beds")
        x_encoding = alt.X("Number_Beds:N", scale=alt.Scale(paddingInner=0.5), title="Number of Bedrooms")
        box = alt.Chart(stats_bedrooms).mark_bar().encode(
            x=x_encoding, y=alt.Y("Q1:Q", title="Price"), y2="Q3:Q", color="Number_Beds:N",
            tooltip=["Number_Beds:N", alt.Tooltip("Max:Q", format="$,.0f"), alt.Tooltip("Q3:Q", format="$,.0f"),
                     alt.Tooltip("median:Q", format="$,.0f"), alt.Tooltip("Q1:Q", format="$,.0f"),
                     alt.Tooltip("Min:Q", format="$,.0f")]
        )
        median = alt.Chart(stats_bedrooms).mark_tick(color="white", size=20).encode(
            x=x_encoding, y="median:Q",
            tooltip=["Number_Beds:N", alt.Tooltip("Max:Q", format="$,.0f"), alt.Tooltip("Q3:Q", format="$,.0f"),
                     alt.Tooltip("median:Q", format="$,.0f"), alt.Tooltip("Q1:Q", format="$,.0f"),
                     alt.Tooltip("Min:Q", format="$,.0f")]
        )
        whiskers = (
            alt.Chart(stats_bedrooms).mark_rule().encode(x=x_encoding, y="Min:Q", y2="Q1:Q", color="Number_Beds:N",
                                                         tooltip=["Number_Beds:N", alt.Tooltip("Min:Q", format="$,.0f")]) +
            alt.Chart(stats_bedrooms).mark_rule().encode(x=x_encoding, y="Q3:Q", y2="Max:Q", color="Number_Beds:N",
                                                         tooltip=["Number_Beds:N", alt.Tooltip("Max:Q", format="$,.0f")])
        )
        outliers = alt.Chart(outliers_bedrooms[outliers_bedrooms["is_outlier"]]).mark_point().encode(
            x=x_encoding, y="Price:Q", color="Number_Beds:N",
            tooltip=["Number_Beds:N", alt.Tooltip("Price:Q", format="$,.0f")]
        )
        chart = (whiskers + box + median + outliers).properties(
            width="container", height="container", title="Price vs Number of Bedrooms"
        ).configure_title(fontSize=25, font="Roboto, sans-serif", color="#000000", anchor="middle"
        ).configure_axis(labelFontSize=CHART_AXIS_TICKFONT_FONT_SIZE, titleFontSize=CHART_AXIS_TITLE_FONT_SIZE
        ).configure_view(strokeWidth=0)
        chart_spec = chart.to_dict(format="vega")
        chart_spec["autosize"] = {"type": "fit", "contains": "padding"}
        return chart_spec

    # Callback 5: Update Chart 3 (Bubble Chart)
    @app.callback(
        Output("chart3", "figure"),
        Input('filtered-data', 'data')
    )
    def update_chart3(data):
        if not data:
            fig = go.Figure()
            fig.update_layout(
                title="Median House Price to Family Income Ratio by City",
                xaxis_title="City", yaxis_title="Price to Income Ratio", template="plotly_white"
            )
            return fig
        df = pd.DataFrame(data)
        city_data = df.groupby("City").agg({
            "Price": "median", "Median_Family_Income": "median", "Population": "first", "Province": "first"
        }).reset_index()
        city_data["Price_Income_Ratio"] = city_data["Price"] / city_data["Median_Family_Income"]
        fig = px.scatter(
            city_data, x="City", y="Price_Income_Ratio", size="Population", color="Province",
            hover_name="City", custom_data=["Price", "Province"],
            title="Median House Price to Family Income Ratio by City", template="plotly_white", size_max=60
        )
        fig.update_traces(
            marker=dict(sizemin=15),
            hovertemplate=(
                "<b>%{hovertext}</b><br>Province: %{customdata[1]}<br>Population: %{marker.size:,.0f}<br>" +
                "Median Price: %{customdata[0]:$,.0f}<br>Price-Income Ratio: %{y:.2f}<extra></extra>"
            )
        )
        fig.update_layout(
            xaxis_title="City", yaxis_title="Price to Family Income Ratio", xaxis_tickangle=-45,
            title=dict(text="Median House Price to Family Income Ratio by City", font=dict(size=25, family="Roboto, sans-serif", color="#000000"),
                       x=0.5, y=0.95, xanchor="center", yanchor="top"),
            xaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE, yaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,
            xaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE, yaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,
            plot_bgcolor="#F5F5F5", paper_bgcolor="#FFFFFF", margin=dict(l=10, r=10, t=50, b=10)
        )
        return fig

    # Callback 6: Update Map
    @app.callback(
        Output("map", "spec"),
        Input('filtered-data', 'data')
    )
    def update_map(data):
        if not data:
            return alt.Chart(pd.DataFrame()).mark_text().encode(
                text=alt.value("No Data Available")
            ).properties(
                title="Map of Canadian Provinces", width=600, height=400
            ).to_dict()
        df = pd.DataFrame(data)
        wikipedia_data = pd.DataFrame({
            "name": df["Province"].unique(),
            "wikipedia": [f"https://en.wikipedia.org/wiki/{prov.replace(' ', '_')}" for prov in df["Province"].unique()]
        })
        agg_df = df.groupby(["City", "Province"]).agg({
            "Price": "median", "Number_Beds": "mean"
        }).reset_index()
        map_df = pd.merge(agg_df, df_locations, on=["City", "Province"], how="left")

        if "Halifax" in map_df["City"].values:
            map_df.loc[map_df["City"] == "Halifax", "Latitude"] = 44.6488
            map_df.loc[map_df["City"] == "Halifax", "Longitude"] = -63.5752
        base_map = alt.Chart(alt.Data(values=geojson_data['features'])).mark_geoshape(stroke='white').project(
            'transverseMercator', rotate=[90, 0, 0]
        ).encode(
            tooltip=alt.Tooltip('properties.name:N', title="Province"),
            color=alt.Color('properties.name:N', scale=alt.Scale(scheme='tableau20'), legend=None),
            href='wikipedia:N'
        ).transform_lookup(
            lookup='properties.name', from_=alt.LookupData(wikipedia_data, 'name', ['wikipedia'])
        )
        city_markers = alt.Chart(map_df).mark_circle().encode(
            longitude='Longitude:Q', latitude='Latitude:Q',
            color=alt.Color('Price:Q', scale=alt.Scale(scheme='viridis')),
            size=alt.Size('Price:Q', scale=alt.Scale(range=[50, 500])),
            tooltip=["City:N", alt.Tooltip('Price:Q', title="Median Price", format=",.0f"),
                     alt.Tooltip('Number_Beds:Q', title="Average Bedrooms", format=".2f")]
        )
        final_map = (base_map + city_markers).properties(
            width="container", height="container", title="Map of Canadian Provinces with Selected Cities"
        ).configure_title(fontSize=25, font='Roboto, sans-serif', color="#000000", anchor='middle')
        return final_map.to_dict(format="vega")

# from dash import Output, Input
# from dash import html
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import altair as alt
# from src.utils.data_loader import load_data
# import requests  # For fetching GeoJSON data
# from functools import lru_cache  # Added for caching

# # Load the datasets once when the module is imported
# df_locations, df_housing = load_data()

# # Define constants for chart styling
# CHART_AXIS_TITLE_FONT_SIZE = 18
# CHART_AXIS_TICKFONT_FONT_SIZE = 16

# # Enable vegafusion for better Altair performance with large datasets
# alt.data_transformers.enable("vegafusion")

# # Fetch GeoJSON data
# geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/canada.geojson"
# try:
#     response = requests.get(geojson_url)
#     response.raise_for_status()  # Raise an error if the request fails
#     geojson_data = response.json()
# except requests.exceptions.RequestException as e:
#     print(f"Error fetching GeoJSON: {e}")
#     geojson_data = {"features": []}  # Fallback to empty data

# @lru_cache(maxsize=1024)
# def get_filtered_data(selected_cities: tuple, selected_provinces: tuple, 
#                       bedrooms_range: tuple, bathrooms_range: tuple):
#     """
#     Filter the global df_housing DataFrame based on the provided parameters.

#     Args:
#         selected_cities: Tuple of selected cities.
#         selected_provinces: Tuple of selected provinces.
#         bedrooms_range: Tuple of (min, max) bedrooms.
#         bathrooms_range: Tuple of (min, max) bathrooms.

#     Returns:
#         Filtered DataFrame.
#     """
#     filtered_df = df_housing.copy()
#     if selected_cities:
#         filtered_df = filtered_df[filtered_df["City"].isin(selected_cities)]
#     if selected_provinces:
#         filtered_df = filtered_df[filtered_df["Province"].isin(selected_provinces)]
#     # Always apply range filters since sliders provide default values
#     filtered_df = filtered_df[(filtered_df["Number_Beds"] >= bedrooms_range[0]) & 
#                               (filtered_df["Number_Beds"] <= bedrooms_range[1])]
#     filtered_df = filtered_df[(filtered_df["Number_Baths"] >= bathrooms_range[0]) & 
#                               (filtered_df["Number_Baths"] <= bathrooms_range[1])]
#     return filtered_df

# def register_callbacks(app):
#     """
#     Register callbacks for the Dash application to update the dashboard
#     based on user inputs.
    
#     Args:
#         app: The Dash application instance.
#     """
#     @app.callback(
#         [Output("median-price", "children"),
#          Output("avg-bedrooms", "children"),
#          Output("avg-bathrooms", "children"),
#          Output("price-range", "children"),
#          Output("chart1", "spec"),
#          Output("chart2", "spec"),
#          Output("chart3", "figure"),
#          Output("map", "spec")],
#         [Input("city-filter", "value"),
#          Input("province-filter", "value"),
#          Input("bedrooms-slider", "value"),
#          Input("bathrooms-slider", "value")]
#     )
#     def update_dashboard(selected_cities, selected_provinces, bedrooms_range, bathrooms_range):
#         """
#         Update the dashboard's summary statistics and charts based on user inputs.
        
#         Args:
#             selected_cities: List of selected cities from the city filter.
#             selected_provinces: List of selected provinces from the province filter.
#             bedrooms_range: Tuple of min and max bedrooms from the slider.
#             bathrooms_range: Tuple of min and max bathrooms from the slider.
        
#         Returns:
#             Tuple containing updated HTML components for summary statistics and
#             chart specifications/figures.
#         """
#         # Convert lists to tuples for caching
#         selected_cities_tuple = tuple(selected_cities) if selected_cities else tuple()
#         selected_provinces_tuple = tuple(selected_provinces) if selected_provinces else tuple()
#         bedrooms_range_tuple = tuple(bedrooms_range)
#         bathrooms_range_tuple = tuple(bathrooms_range)
        
#         # Get filtered DataFrame using the cached function
#         filtered_df = get_filtered_data(selected_cities_tuple, selected_provinces_tuple, 
#                                         bedrooms_range_tuple, bathrooms_range_tuple)

#         # Calculate summary statistics
#         median_price = filtered_df["Price"].median()
#         avg_bedrooms = filtered_df["Number_Beds"].mean()
#         avg_bathrooms = filtered_df["Number_Baths"].mean()
#         min_price = filtered_df["Price"].min()
#         max_price = filtered_df["Price"].max()

#         # Optimized function to compute boxplot statistics for a given group
#         def compute_boxplot_stats(group_df, group_col):
#             """
#             Compute boxplot statistics (quartiles, whiskers, outliers) for a grouped column.
            
#             Args:
#                 group_df: DataFrame to compute statistics on.
#                 group_col: Column name to group by.
            
#             Returns:
#                 Tuple of (stats DataFrame, DataFrame with outlier flags).
#             """
#             stats = group_df.groupby(group_col)["Price"].describe().reset_index()
#             stats = stats.rename(columns={'25%': 'Q1', '50%': 'median', '75%': 'Q3'})
#             stats['IQR'] = stats['Q3'] - stats['Q1']
#             stats['whisker_low_limit'] = stats['Q1'] - 1.5 * stats['IQR']
#             stats['whisker_high_limit'] = stats['Q3'] + 1.5 * stats['IQR']

#             # Merge whisker limits back into the original DataFrame
#             group_df = group_df.merge(stats[[group_col, 'whisker_low_limit', 'whisker_high_limit']], 
#                                      on=group_col, how='left')

#             # Compute whisker ends using vectorized operations
#             whisker_low = group_df[group_df['Price'] >= group_df['whisker_low_limit']]\
#                              .groupby(group_col)['Price'].min().rename('Min')
#             whisker_high = group_df[group_df['Price'] <= group_df['whisker_high_limit']]\
#                               .groupby(group_col)['Price'].max().rename('Max')

#             # Combine into stats
#             stats = stats.merge(whisker_low, on=group_col, how='left')
#             stats = stats.merge(whisker_high, on=group_col, how='left')

#             # Identify outliers
#             group_df['is_outlier'] = (group_df['Price'] < group_df['whisker_low_limit']) | \
#                                      (group_df['Price'] > group_df['whisker_high_limit'])

#             return stats, group_df

#         # Chart 1: City Price Distribution (Altair Boxplot)
#         if not filtered_df.empty:
#             stats_city, outliers_city = compute_boxplot_stats(filtered_df, "City")

#             # Compute the sorted order based on median price
#             city_medians = filtered_df.groupby("City")["Price"].median().sort_values()
#             sorted_cities = city_medians.index.tolist()

#             # Define the x-encoding with sorting by median price
#             x_encoding_city = alt.X("City:N", scale=alt.Scale(paddingInner=0.5), title="City", sort=sorted_cities)

#             # Boxes (Q1 to Q3)
#             box_city = alt.Chart(stats_city).mark_bar().encode(
#                 x=x_encoding_city,
#                 y=alt.Y("Q1:Q", title="Price"),
#                 y2="Q3:Q",
#                 color="City:N",
#                 tooltip=[
#                     alt.Tooltip("City:N", title="City"),
#                     alt.Tooltip("Max:Q", title="Max", format="$,.0f"),
#                     alt.Tooltip("Q3:Q", title="Q3", format="$,.0f"),
#                     alt.Tooltip("median:Q", title="Median", format="$,.0f"),
#                     alt.Tooltip("Q1:Q", title="Q1", format="$,.0f"),
#                     alt.Tooltip("Min:Q", title="Min", format="$,.0f")
#                 ]
#             )

#             # Median line
#             median_city = alt.Chart(stats_city).mark_tick(color="white", size=20).encode(
#                 x=x_encoding_city,
#                 y="median:Q",
#                 tooltip=[
#                     alt.Tooltip("City:N", title="City"),
#                     alt.Tooltip("Max:Q", title="Max", format="$,.0f"),
#                     alt.Tooltip("Q3:Q", title="Q3", format="$,.0f"),
#                     alt.Tooltip("median:Q", title="Median", format="$,.0f"),
#                     alt.Tooltip("Q1:Q", title="Q1", format="$,.0f"),
#                     alt.Tooltip("Min:Q", title="Min", format="$,.0f")
#                 ]
#             )

#             # Whiskers (low and high)
#             whiskers_city = (
#                 alt.Chart(stats_city).mark_rule().encode(
#                     x=x_encoding_city,
#                     y="Min:Q",
#                     y2="Q1:Q",
#                     color="City:N",
#                     tooltip=[
#                         alt.Tooltip("City:N", title="City"),
#                         alt.Tooltip("Min:Q", title="Min", format="$,.0f")
#                     ]
#                 ) + alt.Chart(stats_city).mark_rule().encode(
#                     x=x_encoding_city,
#                     y="Q3:Q",
#                     y2="Max:Q",
#                     color="City:N",
#                     tooltip=[
#                         alt.Tooltip("City:N", title="City"),
#                         alt.Tooltip("Max:Q", title="Max", format="$,.0f")
#                     ]
#                 )
#             )

#             # Outliers
#             outliers_plot_city = alt.Chart(outliers_city[outliers_city["is_outlier"]]).mark_point().encode(
#                 x=x_encoding_city,
#                 y="Price:Q",
#                 color="City:N",
#                 tooltip=[
#                     alt.Tooltip("City:N", title="City"),
#                     alt.Tooltip("Price:Q", title="Price", format="$,.0f")
#                 ]
#             )

#             # Combine all layers for Chart 1
#             chart1 = (whiskers_city + box_city + median_city + outliers_plot_city).properties(
#                 width="container",
#                 height="container",
#                 title="City Price Distribution (Sorted by Median Price)"
#             ).configure_title(
#                 fontSize=25,
#                 font="Roboto, sans-serif",
#                 color="#000000",
#                 anchor="middle"
#             ).configure_axis(
#                 labelFontSize=CHART_AXIS_TICKFONT_FONT_SIZE,
#                 titleFontSize=CHART_AXIS_TITLE_FONT_SIZE
#             ).configure_view(
#                 strokeWidth=0
#             )
#             chart1_spec = chart1.to_dict(format="vega")
#             chart1_spec["autosize"] = {"type": "fit", "contains": "padding"}
#         else:
#             chart1_spec = alt.Chart(pd.DataFrame()).mark_text().encode(
#                 text=alt.value("No Data Available")
#             ).properties(
#                 title="City Price Distribution (Sorted by Median Price)",
#                 width=600,
#                 height=400
#             ).configure_title(
#                 fontSize=25,
#                 font="Roboto, sans-serif",
#                 color="#000000",
#                 anchor="middle"
#             ).to_dict()

#         # Chart 2: Price vs Number of Bedrooms (Altair Boxplot)
#         if not filtered_df.empty:
#             stats_bedrooms, outliers_bedrooms = compute_boxplot_stats(filtered_df, "Number_Beds")

#             # Define the x-encoding with increased padding to narrow the boxes
#             x_encoding_bedrooms = alt.X("Number_Beds:N", scale=alt.Scale(paddingInner=0.5), title="Number of Bedrooms")

#             # Boxes (Q1 to Q3)
#             box_bedrooms = alt.Chart(stats_bedrooms).mark_bar().encode(
#                 x=x_encoding_bedrooms,
#                 y=alt.Y("Q1:Q", title="Price"),
#                 y2="Q3:Q",
#                 color="Number_Beds:N",
#                 tooltip=[
#                     alt.Tooltip("Number_Beds:N", title="Number of Bedrooms"),
#                     alt.Tooltip("Max:Q", title="Max", format="$,.0f"),
#                     alt.Tooltip("Q3:Q", title="Q3", format="$,.0f"),
#                     alt.Tooltip("median:Q", title="Median", format="$,.0f"),
#                     alt.Tooltip("Q1:Q", title="Q1", format="$,.0f"),
#                     alt.Tooltip("Min:Q", title="Min", format="$,.0f")
#                 ]
#             )

#             # Median line
#             median_bedrooms = alt.Chart(stats_bedrooms).mark_tick(color="white", size=20).encode(
#                 x=x_encoding_bedrooms,
#                 y="median:Q",
#                 tooltip=[
#                     alt.Tooltip("Number_Beds:N", title="Number of Bedrooms"),
#                     alt.Tooltip("Max:Q", title="Max", format="$,.0f"),
#                     alt.Tooltip("Q3:Q", title="Q3", format="$,.0f"),
#                     alt.Tooltip("median:Q", title="Median", format="$,.0f"),
#                     alt.Tooltip("Q1:Q", title="Q1", format="$,.0f"),
#                     alt.Tooltip("Min:Q", title="Min", format="$,.0f")
#                 ]
#             )

#             # Whiskers (low and high)
#             whiskers_bedrooms = (
#                 alt.Chart(stats_bedrooms).mark_rule().encode(
#                     x=x_encoding_bedrooms,
#                     y="Min:Q",
#                     y2="Q1:Q",
#                     color="Number_Beds:N",
#                     tooltip=[
#                         alt.Tooltip("Number_Beds:N", title="Number of Bedrooms"),
#                         alt.Tooltip("Min:Q", title="Min", format="$,.0f")
#                     ]
#                 ) + alt.Chart(stats_bedrooms).mark_rule().encode(
#                     x=x_encoding_bedrooms,
#                     y="Q3:Q",
#                     y2="Max:Q",
#                     color="Number_Beds:N",
#                     tooltip=[
#                         alt.Tooltip("Number_Beds:N", title="Number of Bedrooms"),
#                         alt.Tooltip("Max:Q", title="Max", format="$,.0f")
#                     ]
#                 )
#             )

#             # Outliers
#             outliers_plot_bedrooms = alt.Chart(outliers_bedrooms[outliers_bedrooms["is_outlier"]]).mark_point().encode(
#                 x=x_encoding_bedrooms,
#                 y="Price:Q",
#                 color="Number_Beds:N",
#                 tooltip=[
#                     alt.Tooltip("Number_Beds:N", title="Number of Bedrooms"),
#                     alt.Tooltip("Price:Q", title="Price", format="$,.0f")
#                 ]
#             )

#             # Combine all layers for Chart 2
#             chart2 = (whiskers_bedrooms + box_bedrooms + median_bedrooms + outliers_plot_bedrooms).properties(
#                 width="container",
#                 height="container",
#                 title="Price vs Number of Bedrooms"
#             ).configure_title(
#                 fontSize=25,
#                 font="Roboto, sans-serif",
#                 color="#000000",
#                 anchor="middle"
#             ).configure_axis(
#                 labelFontSize=CHART_AXIS_TICKFONT_FONT_SIZE,
#                 titleFontSize=CHART_AXIS_TITLE_FONT_SIZE
#             ).configure_view(
#                 strokeWidth=0
#             )
#             chart2_spec = chart2.to_dict(format="vega")
#             chart2_spec["autosize"] = {"type": "fit", "contains": "padding"}
#         else:
#             chart2_spec = alt.Chart(pd.DataFrame()).mark_text().encode(
#                 text=alt.value("No Data Available")
#             ).properties(
#                 title="Price vs Number of Bedrooms",
#                 width=600,
#                 height=400
#             ).configure_title(
#                 fontSize=25,
#                 font="Roboto, sans-serif",
#                 color="#000000",
#                 anchor="middle"
#             ).to_dict()

#         # Chart 3: Bubble Chart - Median House Price to Income Ratio by City (Plotly)
#         if not filtered_df.empty:
#             city_data = filtered_df.groupby("City").agg({
#                 "Price": "median",
#                 "Median_Family_Income": "median",
#                 "Population": "first",
#                 "Province": "first"
#             }).reset_index()
#             city_data["Price_Income_Ratio"] = city_data["Price"] / city_data["Median_Family_Income"]

#             bubble_chart = px.scatter(
#                 city_data,
#                 x="City",
#                 y="Price_Income_Ratio",
#                 size="Population",
#                 color="Province",
#                 hover_name="City",
#                 custom_data=["Price", "Province"],
#                 title="Median House Price to Family Income Ratio by City",
#                 template="plotly_white",
#                 size_max=60
#             )
#             bubble_chart.update_traces(
#                 marker=dict(sizemin=15),
#                 hovertemplate=(
#                     "<b>%{hovertext}</b><br>" +
#                     "Province: %{customdata[1]}<br>" +
#                     "Population: %{marker.size:,.0f}<br>" +
#                     "Median Price: %{customdata[0]:$,.0f}<br>" +
#                     "Price-Income Ratio: %{y:.2f}<extra></extra>"
#                 )
#             )

#             bubble_chart.update_layout(
#                 xaxis_title="City",
#                 yaxis_title="Price to Family Income Ratio",
#                 xaxis_tickangle=-45,
#                 title=dict(
#                     text="Median House Price to Family Income Ratio by City",
#                     font=dict(size=25, family="Roboto, sans-serif", color="#000000"),
#                     x=0.5,
#                     y=0.95,
#                     xanchor="center",
#                     yanchor="top"
#                 ),
#                 xaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,
#                 yaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,
#                 xaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,
#                 yaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,
#                 plot_bgcolor="#F5F5F5",
#                 paper_bgcolor="#FFFFFF",
#                 margin=dict(l=10, r=10, t=50, b=10)
#             )
#         else:
#             bubble_chart = go.Figure()
#             bubble_chart.update_layout(
#                 title="Median House Price to Family Income Ratio by City",
#                 xaxis_title="City",
#                 yaxis_title="Price to Income Ratio",
#                 template="plotly_white"
#             )

#         # Map: Altair-based map of Canadian provinces with city markers
#         wikipedia_data = pd.DataFrame({
#             "name": filtered_df["Province"].unique() if selected_provinces else df_housing["Province"].unique(),
#             "wikipedia": [
#                 f"https://en.wikipedia.org/wiki/{prov.replace(' ', '_')}" for prov in 
#                 (filtered_df["Province"].unique() if selected_provinces else df_housing["Province"].unique())
#             ]
#         })

#         # Compute aggregated stats for map and merge with locations
#         if not filtered_df.empty:
#             agg_df = filtered_df.groupby(["City", "Province"]).agg({
#                 "Price": "median",
#                 "Number_Beds": "mean"
#             }).reset_index()
#             map_df = pd.merge(agg_df, df_locations, on=["City", "Province"], how="left")
#         else:
#             map_df = pd.DataFrame(columns=["City", "Province", "Price", "Number_Beds", "Latitude", "Longitude"])

#         # Adjust Halifax coordinates if present
#         if "Halifax" in map_df["City"].values:
#             map_df.loc[map_df["City"] == "Halifax", "Latitude"] = 44.6488
#             map_df.loc[map_df["City"] == "Halifax", "Longitude"] = -63.5752

#         base_map = alt.Chart(
#             alt.Data(values=geojson_data['features'])
#         ).mark_geoshape(
#             stroke='white'
#         ).project(
#             'transverseMercator',
#             rotate=[90, 0, 0]
#         ).encode(
#             tooltip=alt.Tooltip('properties.name:N', title="Province"),
#             color=alt.Color('properties.name:N', scale=alt.Scale(scheme='tableau20'), legend=None),
#             href='wikipedia:N'
#         ).transform_lookup(
#             lookup='properties.name',
#             from_=alt.LookupData(wikipedia_data, 'name', ['wikipedia'])
#         )

#         city_markers = alt.Chart(map_df).mark_circle().encode(
#             longitude='Longitude:Q',
#             latitude='Latitude:Q',
#             color=alt.Color('Price:Q', scale=alt.Scale(scheme='viridis')),
#             size=alt.Size('Price:Q', scale=alt.Scale(range=[50, 500])),
#             tooltip=[
#                 alt.Tooltip('City:N', title="City"),
#                 alt.Tooltip('Price:Q', title="Median Price", format=",.0f"),
#                 alt.Tooltip('Number_Beds:Q', title="Average Bedrooms", format=".2f")
#             ]
#         )

#         final_map = (base_map + city_markers).properties(
#             width="container",
#             height="container",
#             title="Map of Canadian Provinces with Selected Cities"
#         ).configure_title(
#             fontSize=25,
#             font='Roboto, sans-serif',
#             color="#000000",
#             anchor='middle'
#         )

#         # Return updated content
#         return (
#             html.Div([
#                 html.H5("Median Price", style={"margin": "0", "color": "#FFFFFF"}),
#                 html.H3(f"${median_price:,.0f}", style={"margin": "0", "color": "#1E88E5"})
#             ]),
#             html.Div([
#                 html.H5("Average Bedrooms", style={"margin": "0", "color": "#FFFFFF"}),
#                 html.H3(f"{avg_bedrooms:.2f}", style={"margin": "0", "color": "#1E88E5"})
#             ]),
#             html.Div([ 
#                 html.H5("Average Bathrooms", style={"margin": "0", "color": "#FFFFFF"}),
#                 html.H3(f"{avg_bathrooms:.2f}", style={"margin": "0", "color": "#1E88E5"})
#             ]),
#             html.Div([
#                 html.H5("Price Range", style={"margin": "0", "color": "#FFFFFF"}),
#                 html.H3(f"${min_price:,.0f} - ${max_price:,.0f}", style={"margin": "0", "color": "#1E88E5"})
#             ]),
#             chart1_spec,
#             chart2_spec,
#             bubble_chart,
#             final_map.to_dict(format="vega")
#         )