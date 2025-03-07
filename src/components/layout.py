from dash import html, dcc
import dash_bootstrap_components as dbc
from .sidebar import sidebar
from utils.data_loader import load_data

df = load_data()

def serve_layout():
    return dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col(html.H2("Canadian House Prices Dashboard", style={"color": "#FFFFFF"}), width=8)
        ], style={"background-color": "#0E1731", "padding": "10px"}),

        dbc.Row([
            dbc.Col(sidebar(df), width=2, style={"background-color": "#053FA8", "padding": "20px"}),
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Card(html.Div(id="median-price")), width=4),
                    dbc.Col(dbc.Card(html.Div(id="avg-bedrooms")), width=4),
                    dbc.Col(dbc.Card(html.Div(id="price-range")), width=4)
                ], className="mb-3"),

                dbc.Row([
                    dbc.Col(dbc.Card(dcc.Graph(id="map-figure")), width=6),
                    dbc.Col(dbc.Card(dcc.Graph(id="chart1")), width=6)
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(dbc.Card(dcc.Graph(id="chart3")), width=6),
                    dbc.Col(dbc.Card(dcc.Graph(id="chart2")), width=6)
                ], className="mb-4"),
            ], style={"padding": "20px", "background-color": "#FAFDFF"})
        ])
    ])
