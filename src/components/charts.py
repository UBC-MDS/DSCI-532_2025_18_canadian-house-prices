import dash_bootstrap_components as dbc
from dash import dcc

def create_map_card():
    return dbc.Card([
        dbc.CardBody(
            dcc.Graph(id="map", style={"height": "100%"}),
            style={"height": "100%", "background-color": "#FFFFFF", "padding": "10px"}
        )
    ], style={
        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
        "border-radius": "10px",
        "margin": "15px",
        "height": "100%"
    })

def create_chart1_card():
    return dbc.Card([
        dbc.CardBody(
            dcc.Graph(id="chart1", style={"height": "100%"}),
            style={"height": "100%", "background-color": "#FFFFFF", "padding": "10px"}
        )
    ], style={
        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
        "border-radius": "10px",
        "margin": "15px",
        "height": "100%"
    })

def create_chart2_card():
    return dbc.Card([
        dbc.CardBody(
            dcc.Graph(id="chart2", style={"height": "100%"}),
            style={"height": "100%", "background-color": "#FFFFFF", "padding": "10px"}
        )
    ], style={
        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
        "border-radius": "10px",
        "margin": "15px",
        "height": "100%"
    })

def create_chart3_card():
    return dbc.Card([
        dbc.CardBody(
            dcc.Graph(id="chart3", style={"height": "100%"}),
            style={"height": "100%", "background-color": "#FFFFFF", "padding": "10px"}
        )
    ], style={
        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
        "border-radius": "10px",
        "margin": "15px",
        "height": "100%"
    })