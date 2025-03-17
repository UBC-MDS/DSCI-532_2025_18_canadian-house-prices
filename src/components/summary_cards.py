import dash_bootstrap_components as dbc
from dash import html, dcc

SUMMARY_CARD_WIDTH = 3

def create_summary_cards():
    """
    Creates a row of summary cards displaying key housing market metrics.

    Returns:
        dbc.Row: A Bootstrap-styled row containing four summary statistic cards.

    Summary Cards:
        - Median Price
        - Average Number of Bedrooms
        - Average Number of Bathrooms
        - Price Range
    """
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

    ], className="flex-grow-1", style={"height": "5vh"})
