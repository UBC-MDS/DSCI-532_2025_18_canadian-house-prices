import dash_bootstrap_components as dbc
from dash import html
from components.sidebar import sidebar
from components.summary_cards import summary_cards
from components.charts import charts_section

def create_layout():
    """Returns the main app layout."""
    return dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col(html.H2("Canadian House Prices Dashboard", style={"color": "#FFFFFF", "text-align": "left"}), width=8)
        ], style={"background-color": "#0E1731", "padding": "10px", "box-shadow": "0 2px 5px 0 rgba(0,0,0,0.2)"}),

        dbc.Row([
            dbc.Col(sidebar, width=2, style={"background-color": "#053FA8", "padding": "20px", "box-shadow": "2px 0 5px 0 rgba(0,0,0,0.2)"}),
            dbc.Col([summary_cards, charts_section], className="mb-3", style={"padding-top": "20px", "background-color": "#FAFDFF"})
        ])
    ])
