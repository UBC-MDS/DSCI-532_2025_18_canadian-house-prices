import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
from src.components.sidebar import create_sidebar
from src.components.summary_cards import create_summary_cards
from src.components.charts import create_map_card, create_chart1_card, create_chart2_card, create_chart3_card

def create_layout(df):
    return dbc.Container(fluid=True, children=[
        # Header Row with title
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

        # Button to Toggle Footer
        dbc.Row([
            dbc.Col(
                dbc.Button(
                    "Show Footer",
                    id="footer-toggle-button",
                    color="primary",
                    style={"background-color": "#053FA8", "color": "#FFFFFF", "border-color": "#053FA8", "font-size": "18px"},
                    className="mt-4"
                ),
                width=12
            )
        ], className="mb-4"),


        # Static Footer (always visible)
        dbc.Row([
            dbc.Col(
                html.Div(
                    children=[
                        html.P("This project was done by Fazeeia Mohammed, Colombe Tolokin, Dominic Lam, and HUI Tang."),
                        html.P("The aim is to provide information on the pricing of houses as the location changes across Canada.")
                    ],
                    style={
                        "background-color": "#053FA8",
                        "color": "#FFFFFF",
                        "padding": "20px",
                        "text-align": "center",
                        "position": "fixed",
                        "bottom": "0",
                        "width": "100%",
                        "box-shadow": "0 2px 5px 0 rgba(0,0,0,0.2)"
                    }
                ),
                width=12
            )
        ])
    ])