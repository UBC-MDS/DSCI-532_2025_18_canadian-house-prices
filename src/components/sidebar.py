import dash_bootstrap_components as dbc
from dash import html, dcc

def create_sidebar(df):
    """
    Creates the sidebar component for the Canadian House Prices Dashboard.

    Args:
        df (pd.DataFrame): The dataset used for populating sidebar filter options.

    Returns:
        dbc.Col: A Bootstrap-styled column containing filters, buttons, and additional information.
    
    Sidebar Components:
        - Dashboard Title
        - Description
        - Province Multi-Select Dropdown
        - City Multi-Select Dropdown
        - Bedrooms Range Slider
        - Bathrooms Range Slider
        - Reset Filters Button
        - GitHub & About Buttons
        - About Information (Toggled)
    """
    print("create_sidebar called from components/sidebar.py")
    return dbc.Col([
        html.H3("Canadian House Prices Dashboard", className="mb-4", style={"color": "#FFFFFF", "font-weight": "bold"}),
        
        html.Hr(style={
            "border": "none",
            "border-top": "1px solid #FFFFFF",
            "margin-bottom": "20px"
        }),

        html.P(
            "This dashboard is designed to offer valuable insights into the Canadian real estate market.",
            style={"color": "#FFFFFF", "font-size": "16px", "margin-bottom": "20px"}
        ),
        
        html.Hr(style={
            "border": "none",
            "border-top": "1px solid #FFFFFF",
            "margin-bottom": "20px"
        }),

        # Province Multi-Select Dropdown (Top)
        dbc.Row([
            html.H5("Province", className="mb-4", style={"color": "#FFFFFF"}),
            dcc.Dropdown(
                id="province-filter",
                options=[{"label": province, "value": province} for province in df["Province"].unique()],
                multi=True,
                placeholder="Select Province"
                )
            ], className="mb-4"),
        
        # Add a break between Province and City
        html.Br(),
        
        # City Dropdown Menu
        dbc.Row([
            html.H5("City", className="mb-4", style={"color": "#FFFFFF"}),
            dcc.Dropdown(
                id="city-filter",
                options=[{"label": city, "value": city} for city in df["City"].unique()],
                multi=True,
                placeholder="Select City",
                value=["Vancouver", "Toronto", "Montreal", "Ottawa"]
                )
            ], className="mb-4"),
        
        # Add a break between City and other filters
        html.Br(),
        
        # Bedrooms Range Slider
        dbc.Row([
            html.H5("Bedrooms", className="mb-4", style={"color": "#FFFFFF"}),
            dcc.RangeSlider(
                id="bedrooms-slider",
                min=df["Number_Beds"].min(),
                max=df["Number_Beds"].max(),
                step=1,
                marks={i: str(i) for i in range(df["Number_Beds"].min(), df["Number_Beds"].max() + 1)},
                tooltip={"always_visible": True, "placement": "bottom"},
                value=[df["Number_Beds"].min(), df["Number_Beds"].max()]
                )
            ], className="mb-4"),
        
        # Bathrooms Range Slider
        dbc.Row([
            html.H5("Bathrooms", className="mb-4", style={"color": "#FFFFFF"}),
            dcc.RangeSlider(
                id="bathrooms-slider",
                min=df["Number_Baths"].min(),
                max=df["Number_Baths"].max(),
                step=1,
                marks={i: str(i) for i in range(df["Number_Baths"].min(), df["Number_Baths"].max() + 1)},
                tooltip={"always_visible": True, "placement": "bottom"},
                value=[df["Number_Baths"].min(), df["Number_Baths"].max()]
                )
            ], className="mb-4"),
        
        # Reset Filters Button
        dbc.Row([
            dbc.Col(
                dbc.Button(
                    "Reset Filters",
                    id="reset-button",
                    color="primary",
                    style={"background-color": "#0E1731", "color": "#FFFFFF", "border-color": "#053FA8", "font-size": "20px"},
                    className="mt-2"
                    ),
                width=12
                )
            ], className="mb-4"),

        # GitHub and About Buttons
        dbc.Row([
            dbc.Col(
                dbc.Button(
                    "GitHub",
                    id="github-button",
                    href="https://github.com/UBC-MDS/DSCI-532_2025_18_canadian-house-prices/tree/feat/dom-M3-joel-feedback-address",  # Replace with your repo URL
                    target="_blank",
                    color="secondary",
                    style={"background-color": "#0E1731", "color": "#FFFFFF", "border-color": "#053FA8", "font-size": "20px"},
                    className="mt-2 me-2"  # Added me-2 for right margin
                    ),
                width="auto"  # Use width="auto" to fit content
                ),
            dbc.Col(
                dbc.Button(
                    "About",
                    id="about-button",
                    color="secondary",
                    style={"background-color": "#0E1731", "color": "#FFFFFF", "border-color": "#053FA8", "font-size": "20px"},
                    className="mt-2"
                    ),
                width="auto"  # Use width="auto" to fit content
                )
        ], className="mb-4", style={"justify-content": "flex-start"}),  # Left-align the row
        
        # Hidden About Text (toggled by the About button)
        html.Div(
            id="about-text",
            children=[
            html.P(
                "This project was done by Dominic Lam, Fazeeia Mohammed, Hui Tang, and Colombe Tolokin.",
                style={"color": "#FFFFFF", "font-size": "20px"}
                ),
            html.P(
                "The aim is to provide information on the pricing of houses as the location changes across Canada.",
                style={"color": "#FFFFFF", "font-size": "20px"}
                ),
            html.P(
                "Last Deployment Date: March 17, 2025",
                style={"color": "#FFFFFF", "font-size": "20px"}
                )
            ],
            style={"display": "none"}  # Initially hidden
            )
        
        ],  className = "sidebar mb-2", width=2, style={"width": "14%"} 

        )
