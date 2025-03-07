import dash
import dash_bootstrap_components as dbc
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from components.layout import create_layout
from callbacks.filters import register_filter_callbacks
from callbacks.charts import register_chart_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = create_layout()

register_filter_callbacks(app)
register_chart_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=False)
