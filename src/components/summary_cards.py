import dash_bootstrap_components as dbc
from dash import html, dcc

def create_summary_cards():
    return dbc.Row([

        dbc.Col(
            dcc.Loading(
                dbc.Card(
                    html.Div(id="median-price", className="text-center"),
                    style={
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "10px",
                        "padding": "10px",
                        "background-color": "#0E1731"
                    }
                )
            ),
            width=4
        ),
        dbc.Col(
            dcc.Loading(
                dbc.Card(
                    html.Div(id="avg-bedrooms", className="text-center"),
                    style={
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "10px",
                        "padding": "10px",
                        "background-color": "#0E1731"
                    }
                )
            ),
            width=4
        ),
        dbc.Col(
            dcc.Loading(
                dbc.Card(
                    html.Div(id="price-range", className="text-center"),
                    style={
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "10px",
                        "padding": "10px",
                        "background-color": "#0E1731"
                    }
                )
            ),
            width=4
        )
    ], className="mb-3")