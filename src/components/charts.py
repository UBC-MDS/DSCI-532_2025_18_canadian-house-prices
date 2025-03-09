import dash_bootstrap_components as dbc
from dash import dcc
from dash_vega_components import Vega


def create_map_card():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    Vega(
                        id="map",
                        spec={},
                        opt={"renderer": "canvas", "actions": False},
                        style={"width": "100%", "height": "100%"}
                    )
                ],
                style={"height": "500px"}  # Fixed height for the card body
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