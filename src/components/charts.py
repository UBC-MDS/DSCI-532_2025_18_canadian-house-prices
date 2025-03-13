import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_vega_components import Vega

CHARTS_HEIGHT= "40vh"

def create_map_card():
    return dbc.Card(
        [
            dcc.Loading(
                dbc.CardBody(
                    [
                        Vega(
                            id="map",
                            spec={},
                            opt={"renderer": "canvas", "actions": False},
                            style={"width": "100%", "height": "100%"}
                        )
                    ],
                    style={"height": CHARTS_HEIGHT}  # Fixed height for the card body
                )
            )
        ], style={
        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
        "border-radius": "10px",
        "margin": "15px",
        "height": "100%"
    })
    
def create_chart1_card():
    return dbc.Card([
        dcc.Loading(
            dbc.CardBody(
                [
                    Vega(
                        id="chart1",
                        spec={},  # Initial empty spec, updated by callback
                        opt={"renderer": "canvas", "actions": False},
                        style={"width": "100%", "height": "100%"}
                    )
                ],
                style={"height": CHARTS_HEIGHT, "background-color": "#FFFFFF", "padding": "10px"}
            )
        )
    ], style={
        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
        "border-radius": "10px",
        "margin": "15px",
        "height": "100%"
    })

def create_chart2_card():
    return dbc.Card([
        dcc.Loading(
            dbc.CardBody(
                [
                    Vega(
                        id="chart2",
                        spec={},  # Initial empty spec, updated by callback
                        opt={"renderer": "canvas", "actions": False},  # Disable Vega toolbar
                        style={"width": "100%", "height": "100%"}
                    )
                ],
                style={"height": CHARTS_HEIGHT, "background-color": "#FFFFFF", "padding": "10px"}
            )
        )
    ], style={
        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
        "border-radius": "10px",
        "margin": "15px",
        "height": "100%"
    })

def create_chart3_card():
    return dbc.Card([
        dcc.Loading(
            dbc.CardBody(
            dcc.Graph(id="chart3", style={"height": "100%"}),
                style={"height": CHARTS_HEIGHT, "background-color": "#FFFFFF", "padding": "10px"}
            )
        )
    ], style={
        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
        "border-radius": "10px",
        "margin": "15px",
        "height": CHARTS_HEIGHT
    })