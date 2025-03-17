import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
from src.components.sidebar import create_sidebar
from src.components.summary_cards import create_summary_cards
from src.components.charts import create_map_card, create_chart1_card, create_chart2_card, create_chart3_card

def create_layout(df):
    """
    Creates the main layout of the Dash application.

    Args:
        df (pd.DataFrame): The dataset used for populating sidebar filters.

    Returns:
        dbc.Container: A Bootstrap container containing the full dashboard layout.
    
    Layout Structure:
        - Sidebar (Always Visible)
        - Summary Cards
        - First Row: Map and City Price Distribution Chart
        - Second Row: Price vs Bedrooms and Median Price to Income Ratio Chart
    """
    return dbc.Container(fluid=True, children=[
        dbc.Row([
            create_sidebar(df),  # Sidebar, always visible
            dbc.Col(
                html.Div([
                            # html.Br(),
                            # html.Br(),
                            create_summary_cards(),  # Summary cards
                            html.Br(),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(create_map_card(), width=6, className="h-100"),
                                dbc.Col(create_chart1_card(), width=6, className="h-100")
                            ], className="gx-2 flex-grow-1"),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(create_chart3_card(), width=6, className="h-100"),
                                dbc.Col(create_chart2_card(), width=6, className="h-100")
                            ], className="gx-2 flex-grow-1"),
                            dcc.Store(id='filtered-data', storage_type='memory'),
                        ], className="d-flex flex-column flex-grow-1 mb-2", 
                        style={"background-color": "#FFFFFF", "height": "100vh"})
            )
        ], className="h-100")
    ], style={"height": "100vh"})
