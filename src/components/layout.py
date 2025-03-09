import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
from src.components.sidebar import create_sidebar
from src.components.summary_cards import create_summary_cards
from src.components.charts import create_map_card, create_chart1_card, create_chart2_card, create_chart3_card

def create_layout(df):
    return dcc.Loading(
        id="loading-charts-1",
        type="dot",
        color="#0E1731",
        children=dbc.Container(fluid=True, children=[
            # Main Content Row with sidebar and content area
            dbc.Row([
                create_sidebar(df),  # The sidebar with the reordered filters
                dbc.Col([  # Content Area
                    create_summary_cards(),  # The summary cards
                    dbc.Row([  # First set of charts/cards
                        dbc.Col(create_map_card(), width=6, className="h-100"),
                        dbc.Col(create_chart1_card(), width=6, className="h-100")
                    ], className="gx-2 mb-4", style={"height": "500px"}),

                    dbc.Row([  # Second set of charts/cards
                        dbc.Col(create_chart3_card(), width=6, className="h-100"),
                        dbc.Col(create_chart2_card(), width=6, className="h-100")
                    ], className="gx-2 mb-4", style={"height": "500px"})
                ], className="mb-3", style={"padding-top": "20px", "background-color": "#FAFDFF"})
            ]),
        ])
    )
