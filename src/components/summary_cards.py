import dash_bootstrap_components as dbc
from dash import html, dcc

SUMMARY_CARD_WIDTH = 3

def create_summary_cards():

    return dbc.Row([

        dbc.Col(
            dcc.Loading(
                dbc.Card(
                    html.Div(id="median-price", className="text-center"),
                    className="summary-card"
                )
            ),
            width=SUMMARY_CARD_WIDTH
        ),
        dbc.Col(
            dcc.Loading(
                dbc.Card(
                    html.Div(id="avg-bedrooms", className="text-center"),
                    className="summary-card"
                )
            ),
            width=SUMMARY_CARD_WIDTH
        ),
        dbc.Col(
            dcc.Loading(
                dbc.Card(
                    html.Div(id="avg-bathrooms", className="text-center"),
                    className="summary-card"
                )
            ),
            width=SUMMARY_CARD_WIDTH
        ),
        dbc.Col(
            dcc.Loading(
                dbc.Card(
                    html.Div(id="price-range", className="text-center"),
                    className="summary-card"
                )
            ),
            width=SUMMARY_CARD_WIDTH
        )
    ], className="mb-3")