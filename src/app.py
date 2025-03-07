import dash
import dash_bootstrap_components as dbc
from components.layout import create_layout
from callbacks.filters import register_filter_callbacks
from callbacks.charts import register_chart_callbacks

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server  

app.layout = create_layout()

register_filter_callbacks(app)
register_chart_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=False)  
