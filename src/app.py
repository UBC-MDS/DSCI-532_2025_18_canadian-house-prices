import os
import sys

# Ensure `src/` is in the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import dash
import dash_bootstrap_components as dbc
from components.layout import create_layout
from callbacks.filters import register_filter_callbacks
from callbacks.charts import register_chart_callbacks

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = create_layout()

# Register Callbacks
register_filter_callbacks(app)
register_chart_callbacks(app)

# Expose server for Render deployment
server = app.server  

if __name__ == "__main__":
    app.run_server(debug=False)
