import dash_bootstrap_components as dbc
from dash import html

summary_cards = dbc.Row([
    dbc.Col(dbc.Card(html.Div(id="median-price", className="text-center"), className="p-3"), width=4),
    dbc.Col(dbc.Card(html.Div(id="avg-bedrooms", className="text-center"), className="p-3"), width=4),
    dbc.Col(dbc.Card(html.Div(id="price-range", className="text-center"), className="p-3"), width=4)
], className="mb-3")
