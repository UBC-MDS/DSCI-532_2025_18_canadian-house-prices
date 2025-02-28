import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
file_path = r"data\processed\Cleaned_CanadianHousePrices.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1').dropna()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout
app.layout = dbc.Container(fluid=True, children=[

    # Title
    dbc.Row([ 
        dbc.Col(html.H2("Canadian House Prices Dashboard", className="text-center"), width=12)
    ], className="mb-3"),

   dbc.Row([
       # Filters Panel
       dbc.Col([ 
           html.H3("Filters", className="mb-4"),

           # City Dropdown Menu
           dbc.Row([
               dbc.Label("City", html_for="city-filter", width=12),
               dcc.Dropdown(
                   id="city-filter",
                   options=[{"label": city, "value": city} for city in df["City"].unique()],
                   multi=True, placeholder="Select City"
               )
           ], className="mb-4"),

           # Province Multi-Select Dropdown
           dbc.Row([
               dbc.Label("Province", html_for="province-filter", width=12),
               dcc.Dropdown(
                   id="province-filter",
                   options=[{"label": province, "value": province} for province in df["Province"].unique()],
                   multi=True, placeholder="Select Province"
               )
           ], className="mb-4"),

           # Bedrooms Range Slider
           dbc.Row([
               dbc.Label("Bedrooms", html_for="bedrooms-slider", width=12),
               dcc.RangeSlider(
                   id="bedrooms-slider",
                   min=df["Number_Beds"].min(),
                   max=df["Number_Beds"].max(),
                   step=1,
                   marks={i: str(i) for i in range(df["Number_Beds"].min(), df["Number_Beds"].max() + 1, 1)},
                   tooltip={"always_visible": True, "placement": "bottom"},
                   value=[df["Number_Beds"].min(), df["Number_Beds"].max()]
               )
           ], className="mb-4"),

           # Bathrooms Range Slider
           dbc.Row([
               dbc.Label("Bathrooms", html_for="bathrooms-slider", width=12),
               dcc.RangeSlider(
                   id="bathrooms-slider",
                   min=df["Number_Baths"].min(),
                   max=df["Number_Baths"].max(),
                   step=1,
                   marks={i: str(i) for i in range(df["Number_Baths"].min(), df["Number_Baths"].max() + 1, 1)},
                   tooltip={"always_visible": True, "placement": "bottom"},
                   value=[df["Number_Baths"].min(), df["Number_Baths"].max()]
               )
           ], className="mb-4"),

       ], width=2, className="bg-light p-4 rounded"),

       # Main Container
       dbc.Col([ 
           # Summary Stats
           dbc.Row([ 
               dbc.Col(html.Div(id="median-price", className="border p-2 text-center bg-light"), width=4),
               dbc.Col(html.Div(id="avg-bedrooms", className="border p-2 text-center bg-light"), width=4),
               dbc.Col(html.Div(id="price-range", className="border p-2 text-center bg-light"), width=4)
           ], className="mb-3"),

           # Charts & Map Section
           dbc.Row([ 
               dbc.Col(dbc.Card([
                   dbc.CardHeader("City Price Distribution (Box Plot)"),
                   dbc.CardBody(dcc.Graph(id="chart1", style={"height": "400px", "padding": "5px", "background-color": "lightblue"}))
               ], className="m-1"), width=6),

               dbc.Col(dbc.Card([
                   dbc.CardHeader("Price vs Number of Bedrooms (Scatter Plot)"),
                   dbc.CardBody(dcc.Graph(id="chart2", style={"height": "400px"}))
               ], className="m-1"), width=6)
           ], className="mb-1"),

           dbc.Row([ 
               dbc.Col(dbc.Card([
                   dbc.CardHeader("Median Price Comparison Across Cities (Bar Chart)"),
                   dbc.CardBody(dcc.Graph(id="chart3", style={"height": "400px"}))
               ], className="m-1"), width=6),

               dbc.Col(dbc.Card([
                   dbc.CardHeader("Geospatial Price Distribution (Map)"),
                   dbc.CardBody(dcc.Graph(id="map", style={"height": "500px"}))
               ], className="m-1"), width=6)
           ], className="mb-1")
       ], className="mb-3")
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

    # Summary Stats
    median_price = filtered_df["Price"].median()
    avg_bedrooms = filtered_df["Number_Beds"].mean()
    min_price = filtered_df["Price"].min()
    max_price = filtered_df["Price"].max()

    # City Price Distribution (Box Plot)
    city_price_distribution = px.box(filtered_df, x="City", y="Price", title="City Price Distribution")

    # Price vs Number of Bedrooms (Scatter Plot)
    price_vs_bedrooms = px.scatter(filtered_df, x="Number_Beds", y="Price", title="Price vs Number of Bedrooms")

    # Median Price Comparison Across Cities (Bar Chart)
    city_median_price = filtered_df.groupby('City')['Price'].median().sort_values(ascending=False)
    median_price_comparison = go.Figure(
        data=[go.Bar(
            x=city_median_price.index,
            y=city_median_price.values,
            marker=dict(color='skyblue')
        )],
        layout=go.Layout(
            title="Median Price Across Cities",
            xaxis=dict(title="City"),
            yaxis=dict(title="Median Price (CAD)")
        )
    )

    # Geospatial Price Distribution (Interactive Map)
    geospatial_price_distribution = px.scatter_mapbox(filtered_df, lat='Latitude', lon='Longitude', color='Price', size='Price',
                                                       hover_name='City', title="Geospatial Price Distribution", mapbox_style="open-street-map")
    
    return (
        f"Median Price: ${median_price:,.2f}",
        f"Average Bedrooms: {avg_bedrooms:.2f}",
        f"Price Range: ${min_price:,.2f} - ${max_price:,.2f}",
        city_price_distribution, price_vs_bedrooms, median_price_comparison, geospatial_price_distribution
    )


# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
