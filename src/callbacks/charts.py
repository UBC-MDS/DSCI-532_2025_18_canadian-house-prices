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

# Define a color mapping for Canadian provinces/territories
PROVINCE_COLORS = {
    "British Columbia": "#1F75FE",        # Blue
    "Alberta": "#009E60",                 # Green
    "Saskatchewan": "#FFD700",            # Yellow
    "Manitoba": "#C8102E",                # Red
    "Ontario": "#006341",                 # Dark Green
    "Quebec": "#6A0DAD",                  # Purple
    "New Brunswick": "#FFA500",           # Orange
    "Nova Scotia": "#6CACE4",             # Light Blue
    "Prince Edward Island": "#FFC0CB",    # Pink
    "Newfoundland and Labrador": "#008080", # Teal
    "Northwest Territories": "#8B4513",   # Brown
    "Nunavut": "#DAA520",                 # Gold
    "Yukon": "#32CD32"                    # Lime
}

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

        # Debug: Check if outliers exist
        num_outliers = len(outliers_city[outliers_city["is_outlier"]])
        print(f"Number of outliers detected: {num_outliers}")
        if num_outliers == 0:
            print("No outliers found. Check data range or IQR calculation.")
            print(outliers_city[["City", "Price", "whisker_low_limit", "whisker_high_limit", "is_outlier"]].head())

        city_medians = df.groupby("City")["Price"].median().sort_values()
        sorted_cities = city_medians.index.tolist()
        x_encoding = alt.X("City:N", scale=alt.Scale(paddingInner=0.5), title="City", sort=sorted_cities)
        
        # Merge province data into stats_city for color mapping (keep this)
        city_province_map = df[["City", "Province"]].drop_duplicates()
        stats_city = stats_city.merge(city_province_map, on="City", how="left")
        # Do NOT merge into outliers_city; it already has Province from df

        BAR_WIDTH = 30

        # Box plot with province-based coloring
        box = alt.Chart(stats_city).mark_bar(size=BAR_WIDTH).encode(
            x=x_encoding, y=alt.Y("Q1:Q", title="Price"), y2="Q3:Q",
            color=alt.Color("Province:N", scale=alt.Scale(domain=list(PROVINCE_COLORS.keys()), range=list(PROVINCE_COLORS.values())), legend=None),
            tooltip=["City:N", alt.Tooltip("Max:Q", format="$,.0f"), alt.Tooltip("Q3:Q", format="$,.0f"),
                     alt.Tooltip("median:Q", format="$,.0f"), alt.Tooltip("Q1:Q", format="$,.0f"),
                     alt.Tooltip("Min:Q", format="$,.0f")]
        )
        
        # Median tick
        median = alt.Chart(stats_city).mark_tick(color="white", size=BAR_WIDTH).encode(
            x=x_encoding, y="median:Q",
            tooltip=["City:N", alt.Tooltip("Max:Q", format="$,.0f"), alt.Tooltip("Q3:Q", format="$,.0f"),
                     alt.Tooltip("median:Q", format="$,.0f"), alt.Tooltip("Q1:Q", format="$,.0f"),
                     alt.Tooltip("Min:Q", format="$,.0f")]
        )
        
        # Whiskers with province-based colors
        whiskers = (
            alt.Chart(stats_city).mark_rule().encode(
                x=x_encoding, y="Min:Q", y2="Q1:Q",
                color=alt.Color("Province:N", scale=alt.Scale(domain=list(PROVINCE_COLORS.keys()), range=list(PROVINCE_COLORS.values())), legend=None),
                tooltip=["City:N", alt.Tooltip("Min:Q", format="$,.0f")]
            ) +
            alt.Chart(stats_city).mark_rule().encode(
                x=x_encoding, y="Q3:Q", y2="Max:Q",
                color=alt.Color("Province:N", scale=alt.Scale(domain=list(PROVINCE_COLORS.keys()), range=list(PROVINCE_COLORS.values())), legend=None),
                tooltip=["City:N", alt.Tooltip("Max:Q", format="$,.0f")]
            )
        )
        
        # Outliers with province-based colors, using existing Province column
        outliers = alt.Chart(outliers_city[outliers_city["is_outlier"]]).mark_circle(size=60, stroke="black", strokeWidth=1).encode(
            x=x_encoding, y="Price:Q",
            color=alt.Color("Province:N", scale=alt.Scale(domain=list(PROVINCE_COLORS.keys()), range=list(PROVINCE_COLORS.values())), legend=None),
            tooltip=["City:N", alt.Tooltip("Price:Q", format="$,.0f")]
        )
        
        chart = (whiskers + box + median + outliers).properties(
            width="container", height="container", title="City Price Distribution"
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
        
        box_color = "#4682b4"
        
        # Box plot with fixed color
        box = alt.Chart(stats_bedrooms).mark_bar().encode(
            x=x_encoding, 
            y=alt.Y("Q1:Q", title="Price"), 
            y2="Q3:Q", 
            color=alt.value(box_color),
            tooltip=["No. of Beds:N", alt.Tooltip("Max:Q", format="$,.0f"), alt.Tooltip("Q3:Q", format="$,.0f"),
                     alt.Tooltip("median:Q", format="$,.0f"), alt.Tooltip("Q1:Q", format="$,.0f"),
                     alt.Tooltip("Min:Q", format="$,.0f")]
        )
        
        # Median tick
        median = alt.Chart(stats_bedrooms).mark_tick(color="white", size=20).encode(
            x=x_encoding, 
            y="median:Q",
            tooltip=["No. of Beds:N", alt.Tooltip("Max:Q", format="$,.0f"), alt.Tooltip("Q3:Q", format="$,.0f"),
                     alt.Tooltip("median:Q", format="$,.0f"), alt.Tooltip("Q1:Q", format="$,.0f"),
                     alt.Tooltip("Min:Q", format="$,.0f")]
        )
        
        # Whiskers with the same fixed color
        whiskers = (
            alt.Chart(stats_bedrooms).mark_rule().encode(
                x=x_encoding, 
                y="Min:Q", 
                y2="Q1:Q", 
                color=alt.value(box_color),
                tooltip=["No. of Beds:N", alt.Tooltip("Min:Q", format="$,.0f")]
            ) +
            alt.Chart(stats_bedrooms).mark_rule().encode(
                x=x_encoding, 
                y="Q3:Q", 
                y2="Max:Q", 
                color=alt.value(box_color),
                tooltip=["No. of Beds:N", alt.Tooltip("Max:Q", format="$,.0f")]
            )
        )
        
        # Outliers with the same fixed color
        outliers = alt.Chart(outliers_bedrooms[outliers_bedrooms["is_outlier"]]).mark_point().encode(
            x=x_encoding, 
            y="Price:Q", 
            color=alt.value(box_color),
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
                xaxis_title="City", yaxis_title="Price to Income Ratio", template="plotly_white",
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
            title="Median House Price to Family Income Ratio by City", template="plotly_white", size_max=60,
            color_discrete_map=PROVINCE_COLORS
        )
        
        fig.update_traces(
            marker=dict(sizemin=15),
            hovertemplate=(
                "<b>%{hovertext}</b><br>Province: %{customdata[1]}<br>Population: %{marker.size:,.0f}<br>" +
                "Median Price: %{customdata[0]:$,.0f}<br>Price-Income Ratio: %{y:.2f}<extra></extra>"
            )
        )
        
        fig.update_layout(
            xaxis_title="City", yaxis_title="Price to Income Ratio", xaxis_tickangle=-45,
            title=dict(text="Median House Price to Family Income Ratio by City", 
                       font=dict(size=25, family="Roboto, sans-serif", color="#000000", weight='bold'),
                       x=0.5, y=0.95, xanchor="center", yanchor="top"),
            xaxis=dict(
                title=dict(text="City", font=dict(size=CHART_AXIS_TITLE_FONT_SIZE, family="Roboto, sans-serif", color="#000000", weight='bold')),
                tickfont=dict(size=CHART_AXIS_TICKFONT_FONT_SIZE, family="Roboto, sans-serif", color="#000000", weight='bold')
            ),
            yaxis=dict(
                title=dict(text="Price to Income Ratio", font=dict(size=CHART_AXIS_TITLE_FONT_SIZE, family="Roboto, sans-serif", color="#000000", weight='bold')),
                tickfont=dict(size=CHART_AXIS_TICKFONT_FONT_SIZE, family="Roboto, sans-serif", color="#000000", weight='bold')
            ),
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
            color=alt.Color('properties.name:N', scale=alt.Scale(domain=list(PROVINCE_COLORS.keys()), range=list(PROVINCE_COLORS.values())), legend=None),
        )

        city_markers = alt.Chart(map_df).mark_point(
            shape='triangle-down',
            filled=True,
            opacity=1,          # Low opacity for semi-transparency
        ).encode(
            longitude='Longitude:Q',
            latitude='Latitude:Q',
            color=alt.Color('Price:Q', scale=alt.Scale(scheme='sinebow')),  # More visible color scheme
            size=alt.Size('Price:Q', scale=alt.Scale(range=[50, 500])),
            tooltip=["City:N",
                     alt.Tooltip('Price:Q', title="Median Price", format=",.0f"),
                     alt.Tooltip('Number_Beds:Q', title="Average Bedrooms", format=".2f")]
        )
        
        final_map = (base_map + city_markers).properties(
            width="container", height="container", title="Map of Canadian Provinces with Selected Cities"
        ).configure_title(fontSize=25, font='Roboto, sans-serif', color="#000000", anchor='middle')
        
        return final_map.to_dict(format="vega")