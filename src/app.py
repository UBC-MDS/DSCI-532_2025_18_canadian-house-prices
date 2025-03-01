import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


CHART_AXIS_TITLE_FONT_SIZE = 18
CHART_AXIS_TICKFONT_FONT_SIZE = 16

# Load dataset
file_path = r"data/processed/Cleaned_CanadianHousePrices.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1').dropna()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout
app.layout = dbc.Container(fluid=True, children=[

    dbc.Row([
        dbc.Col(
            html.H2("Canadian House Prices Dashboard", style={"color": "#FFFFFF", "text-align": "left"}),
            width=8
        )
        ], style={
        "background-color": "#0E1731",
        "padding": "10px",
        "box-shadow": "0 2px 5px 0 rgba(0,0,0,0.2)"
    }),


    dbc.Row([
        dbc.Col([
            html.H3("Filters", className="mb-4", style={"color": "#FFFFFF"}),
            # City Dropdown Menu
            dbc.Row([
                # dbc.Label("City", html_for="city-filter", className="mb-4", width=12, style={"color": "#FFFFFF"}),
                html.H5("City", className="mb-4", style={"color": "#FFFFFF"}),
                dcc.Dropdown(
                    id="city-filter",
                    options=[{"label": city, "value": city} for city in df["City"].unique()],
                    multi=True,
                    placeholder="Select City",
                    # Default Selected Cities
                    value=["Vancouver", "Toronto", "Montreal", "Ottawa"]
                )
            ], className="mb-4"),
            # Province Multi-Select Dropdown
            dbc.Row([
                # dbc.Label("Province", html_for="province-filter", width=12, style={"color": "#FFFFFF"}),
                html.H5("Province", className="mb-4", style={"color": "#FFFFFF"}),
                dcc.Dropdown(
                    id="province-filter",
                    options=[{"label": province, "value": province} for province in df["Province"].unique()],
                    multi=True,
                    placeholder="Select Province"
                )
            ], className="mb-4"),
            # Bedrooms Range Slider
            dbc.Row([
                # dbc.Label("Bedrooms", html_for="bedrooms-slider", width=12, style={"color": "#FFFFFF"}),
                html.H5("Bedrooms", className="mb-4", style={"color": "#FFFFFF"}),
                dcc.RangeSlider(
                    id="bedrooms-slider",
                    min=df["Number_Beds"].min(),
                    max=df["Number_Beds"].max(),
                    step=1,
                    marks={i: str(i) for i in range(df["Number_Beds"].min(), df["Number_Beds"].max() + 1)},
                    tooltip={"always_visible": True, "placement": "bottom"},
                    value=[df["Number_Beds"].min(), df["Number_Beds"].max()]
                )
            ], className="mb-4"),
            # Bathrooms Range Slider
            dbc.Row([
                # dbc.Label("Bathrooms", html_for="bathrooms-slider", width=12, style={"color": "#FFFFFF"}),
                html.H5("Bathrooms", className="mb-4", style={"color": "#FFFFFF"}),
                dcc.RangeSlider(
                    id="bathrooms-slider",
                    min=df["Number_Baths"].min(),
                    max=df["Number_Baths"].max(),
                    step=1,
                    marks={i: str(i) for i in range(df["Number_Baths"].min(), df["Number_Baths"].max() + 1)},
                    tooltip={"always_visible": True, "placement": "bottom"},
                    value=[df["Number_Baths"].min(), df["Number_Baths"].max()]
                )
            ], className="mb-4"),

            # Reset Filters Button
            dbc.Row([
                dbc.Col(
                    dbc.Button(
                        "Reset Filters",
                        id="reset-button",
                        color="primary",
                        style={"background-color": "#0E1731", "color": "#FFFFFF", "border-color": "#053FA8", "font-size": "20px"},  # Match sidebar color
                        className="mt-2"
                    ),
                    width=12
                )
            ], className="mb-4")



    dbc.Row([
        dbc.Col([
            html.H3("Filters", className="mb-4", style={"color": "#FFFFFF"}),
            # City Dropdown Menu
            dbc.Row([
                # dbc.Label("City", html_for="city-filter", className="mb-4", width=12, style={"color": "#FFFFFF"}),
                html.H5("City", className="mb-4", style={"color": "#FFFFFF"}),
                dcc.Dropdown(
                    id="city-filter",
                    options=[{"label": city, "value": city} for city in df["City"].unique()],
                    multi=True,
                    placeholder="Select City",
                    # Default Selected Cities
                    value=["Vancouver", "Toronto", "Montreal", "Ottawa"]
                )
            ], className="mb-4"),
            # Province Multi-Select Dropdown
            dbc.Row([
                # dbc.Label("Province", html_for="province-filter", width=12, style={"color": "#FFFFFF"}),
                html.H5("Province", className="mb-4", style={"color": "#FFFFFF"}),
                dcc.Dropdown(
                    id="province-filter",
                    options=[{"label": province, "value": province} for province in df["Province"].unique()],
                    multi=True,
                    placeholder="Select Province"
                )
            ], className="mb-4"),
            # Bedrooms Range Slider
            dbc.Row([
                # dbc.Label("Bedrooms", html_for="bedrooms-slider", width=12, style={"color": "#FFFFFF"}),
                html.H5("Bedrooms", className="mb-4", style={"color": "#FFFFFF"}),
                dcc.RangeSlider(
                    id="bedrooms-slider",
                    min=df["Number_Beds"].min(),
                    max=df["Number_Beds"].max(),
                    step=1,
                    marks={i: str(i) for i in range(df["Number_Beds"].min(), df["Number_Beds"].max() + 1)},
                    tooltip={"always_visible": True, "placement": "bottom"},
                    value=[df["Number_Beds"].min(), df["Number_Beds"].max()]
                )
            ], className="mb-4"),
            # Bathrooms Range Slider
            dbc.Row([
                # dbc.Label("Bathrooms", html_for="bathrooms-slider", width=12, style={"color": "#FFFFFF"}),
                html.H5("Bathrooms", className="mb-4", style={"color": "#FFFFFF"}),
                dcc.RangeSlider(
                    id="bathrooms-slider",
                    min=df["Number_Baths"].min(),
                    max=df["Number_Baths"].max(),
                    step=1,
                    marks={i: str(i) for i in range(df["Number_Baths"].min(), df["Number_Baths"].max() + 1)},
                    tooltip={"always_visible": True, "placement": "bottom"},
                    value=[df["Number_Baths"].min(), df["Number_Baths"].max()]
                )
            ], className="mb-4"),
        ], width=2, style={
            "background-color": "#053FA8",
            "padding": "20px",
            "box-shadow": "2px 0 5px 0 rgba(0,0,0,0.2)"
        }),

       # Main Container
       dbc.Col([ 
           # Summary Stats
           dbc.Row([
            dbc.Col(
                dbc.Card(
                    html.Div(id="median-price", className="text-center"),
                    style={
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "10px",
                        "padding": "10px",
                        "background-color": "#FFFFFF"
                    }
                ),
                width=4
            ),
            dbc.Col(
                dbc.Card(
                    html.Div(id="avg-bedrooms", className="text-center"),
                    style={
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "10px",
                        "padding": "10px",
                        "background-color": "#FFFFFF"
                    }
                ),
                width=4
            ),
            dbc.Col(
                dbc.Card(
                    html.Div(id="price-range", className="text-center"),
                    style={
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "10px",
                        "padding": "10px",
                        "background-color": "#FFFFFF"
                    }
                ),
                width=4
            )
        ], className="mb-3"),  # Adds margin below the row

            # Charts & Map Section - First Row
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody(
                        dcc.Graph(id="map", style={"height": "100%"}),
                        style={"height": "100%", "background-color": "#FFFFFF", "padding": "10px"}
                    )
                ], style={
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                    "border-radius": "10px",
                    "margin": "15px",
                    "height": "100%"
                }), width=6, className="h-100"
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody(
                        dcc.Graph(id="chart1", style={"height": "100%"}),
                        style={"height": "100%", "background-color": "#FFFFFF", "padding": "10px"}
                    )
                ], style={
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                    "border-radius": "10px",
                    "margin": "15px",
                    "height": "100%"
                }), width=6, className="h-100"
            )
        ], className="gx-2 mb-4", style={"height": "500px"}),

        # Additional Charts - Second Row
        dbc.Row([ 
            dbc.Col(
                dbc.Card([
                    dbc.CardBody(
                        dcc.Graph(id="chart3", style={"height": "100%"}),
                        style={"height": "100%", "background-color": "#FFFFFF", "padding": "10px"}
                    )
                ], style={
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                    "border-radius": "10px",
                    "margin": "15px",
                    "height": "100%"
                }), width=6, className="h-100"
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody(
                        dcc.Graph(id="chart2", style={"height": "100%"}),
                        style={"height": "100%", "background-color": "#FFFFFF", "padding": "10px"}
                    )
                ], style={
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                    "border-radius": "10px",
                    "margin": "15px",
                    "height": "100%"
                }), width=6, className="h-100"
            )
        ], className="gx-2 mb-4", style={"height": "500px"})
       ], className="mb-3", style={"padding-top": "20px", "background-color": "#FAFDFF"})
   ])
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

    # Create charts with adjusted margins
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
        xaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,        # X-axis title (e.g., "Cities")
        yaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,        # Y-axis title (e.g., "Price")
        xaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,          # X-axis city names
        yaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,           # Y-axis price values
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=10, r=10, t=50, b=10)  # Reduced margins
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
                xaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,        # X-axis title (e.g., "Cities")
        yaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,        # Y-axis title (e.g., "Price")
        xaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,          # X-axis city names
        yaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,           # Y-axis price values
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=10, r=10, t=50, b=10)  # Reduced margins
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
                    xaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,        # X-axis title (e.g., "Cities")
        yaxis_title_font_size=CHART_AXIS_TITLE_FONT_SIZE,        # Y-axis title (e.g., "Price")
        xaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,          # X-axis city names
        yaxis_tickfont_size=CHART_AXIS_TICKFONT_FONT_SIZE,           # Y-axis price values
            margin=dict(l=10, r=10, t=50, b=10)  # Reduced margins
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
            # height=500
        )
    else:
        geospatial_price_distribution = go.Figure(go.Scattermapbox())
        geospatial_price_distribution.update_layout(
            mapbox_style="carto-positron",
            mapbox_center={"lat": 55.0, "lon": -95.0},
            mapbox_zoom=2,
            height=500,
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
        margin=dict(l=10, r=10, t=50, b=10),  # Reduced margins for map
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


@app.callback(
    Output("city-filter", "options"),
    Input("province-filter", "value")
)
def update_city_options(selected_provinces):
    if selected_provinces and len(selected_provinces) > 0:
        # Filter DataFrame to include only rows with selected provinces
        filtered_df = df[df["Province"].isin(selected_provinces)]
        # Get unique cities from the filtered DataFrame
        city_options = [{"label": city, "value": city} for city in filtered_df["City"].unique()]
    else:
        # If no provinces selected, return all cities
        city_options = [{"label": city, "value": city} for city in df["City"].unique()]
    return city_options

#reset filters
@app.callback(
    [Output("city-filter", "value"),
     Output("province-filter", "value"),
     Output("bedrooms-slider", "value"),
     Output("bathrooms-slider", "value")],
    Input("reset-button", "n_clicks"),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    return (
        ["Vancouver", "Toronto", "Montreal", "Ottawa"],  # Reset city to default
        [],  # Reset province to no selection
        [df["Number_Beds"].min(), df["Number_Beds"].max()],  # Reset bedrooms to full range
        [df["Number_Baths"].min(), df["Number_Baths"].max()]  # Reset bathrooms to full range
    )

@app.callback(
    Output("map-figure", "figure"),
    Input("city-filter", "value")
)
def update_map(selected_cities):
    filtered_df = df.copy()  # Assume df is your full dataset

    # Filter the dataframe based on selected cities
    if selected_cities:  # If the list is not empty
        filtered_df = filtered_df[filtered_df["City"].isin(selected_cities)]

    # Prepare data for the map
    if selected_cities:  # If cities are selected, aggregate data
        map_df = filtered_df.groupby("City").agg({
            "Latitude": "mean",
            "Longitude": "mean",
            "Price": "median",
            "Number_Beds": "mean"
        }).reset_index()
    else:
        map_df = pd.DataFrame()  # Empty dataframe when no cities are selected

    # Create the map figure
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
            height=500
        )
    else:
        geospatial_price_distribution = go.Figure(go.Scattermapbox())
        geospatial_price_distribution.update_layout(
            mapbox_style="carto-positron",
            mapbox_center={"lat": 55.0, "lon": -95.0},
            mapbox_zoom=2,
            height=500,
            title="Geospatial Price Distribution"
        )

    # Add the Canada boundary outline (your updated code)
    geospatial_price_distribution.update_layout(
        mapbox={
            "layers": [{
                "sourcetype": "geojson",
                "source": "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/canada.geojson",
                "type": "line",
                "color": "pink",
                "line": {"width": 1}
            }]
        },
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        title_x=0.5
    )

    return geospatial_price_distribution

# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
