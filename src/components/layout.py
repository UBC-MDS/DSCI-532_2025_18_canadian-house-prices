import dash_bootstrap_components as dbc
from dash import html
from .sidebar import create_sidebar
from .summary_cards import create_summary_cards
from .charts import create_map_card, create_chart1_card, create_chart2_card, create_chart3_card

def create_layout(df):
    return dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col(
                html.H2("Canadian House Prices Dashboard", style={"color": "#FFFFFF", "text-align": "left"}),
                width=8
            )
        ], style={
            "background-color": "#0E1731",
            "padding": "10px",
            "box-shadow": "0 2px 5px 0 rgba(0,0,0,0.2)"
        }),
        dbc.Row([
            create_sidebar(df),
            dbc.Col([
                create_summary_cards(),
                dbc.Row([
                    dbc.Col(create_map_card(), width=6, className="h-100"),
                    dbc.Col(create_chart1_card(), width=6, className="h-100")
                ], className="gx-2 mb-4", style={"height": "500px"}),
                dbc.Row([
                    dbc.Col(create_chart3_card(), width=6, className="h-100"),
                    dbc.Col(create_chart2_card(), width=6, className="h-100")
                ], className="gx-2 mb-4", style={"height": "500px"})
            ], className="mb-3", style={"padding-top": "20px", "background-color": "#FAFDFF"})
        ])
    ])