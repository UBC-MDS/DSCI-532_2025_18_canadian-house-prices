import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_vega_components import Vega

CHARTS_HEIGHT= "40vh"

def create_map_card():
    """
    Creates a card component containing an interactive Vega map.

    Returns:
        dbc.Card: A Bootstrap-styled card containing a Vega map.
    """
    return dbc.Card(
        [
            # dcc.Loading(
            #     dbc.CardBody(
            #         [
            #             Vega(
            #                 id="map",
            #                 spec={},
            #                 opt={"renderer": "canvas", "actions": False},
            #                 style={"width": "100%", "height": "100%"}
            #             )
            #         ],
            #         style={"height": CHARTS_HEIGHT}  # Fixed height for the card body
            #     )
            # )
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
        ], style={
        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
        "border-radius": "10px",
        "margin": "15px",
        "height": "100%"
    })
    
# City Price Distribution
def create_chart1_card():
    """
    Creates a card for the City Price Distribution chart.

    Returns:
        dbc.Card: A card containing a Vega visualization for city price distribution.
    """
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

# Price vs Number of Bedrooms
def create_chart2_card():
    """
    Creates a card for the Price vs Number of Bedrooms chart.

    Returns:
        dbc.Card: A card containing a Vega visualization for price vs. bedrooms.
    """
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
        "height": "97%"
    })

# Median House Price to Family Income Ratio By City
def create_chart3_card():
    """
    Creates a card for the Median House Price to Family Income Ratio by City.

    Returns:
        dbc.Card: A card containing a Dash Graph visualization.
    """
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
        "height": "97%"
    })