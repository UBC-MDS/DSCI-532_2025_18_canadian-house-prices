from dash import Dash
import dash_bootstrap_components as dbc
from src.components.layout import create_layout
from src.utils.data_loader import load_data
from src.callbacks.filters import register_callbacks as register_filters_callbacks
from src.callbacks.charts import register_callbacks as register_charts_callbacks

# Load dataset
df = load_data()

# Initialize Dash application
app = Dash(__name__, title="Canadian House Prices", external_stylesheets=[dbc.themes.BOOTSTRAP])

# Expose Flask server for deployment
server = app.server

# Set the application layout
app.layout = create_layout(df)

# Register application callbacks
register_filters_callbacks(app)
register_charts_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)