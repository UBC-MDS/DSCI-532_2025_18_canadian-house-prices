import dash_bootstrap_components as dbc
from dash import dcc

charts_section = dbc.Row([
    dbc.Col(dbc.Card(dcc.Graph(id="chart1"), className="p-3"), width=6),
    dbc.Col(dbc.Card(dcc.Graph(id="chart2"), className="p-3"), width=6),
    dbc.Col(dbc.Card(dcc.Graph(id="chart3"), className="p-3"), width=6),
    dbc.Col(dbc.Card(dcc.Graph(id="map"), className="p-3"), width=6)
], className="gx-2 mb-4")
