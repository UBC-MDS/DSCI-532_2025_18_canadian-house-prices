from dash import Dash
import dash_bootstrap_components as dbc
from src.components.layout import create_layout
from src.utils.data_loader import load_data
from src.callbacks.filters import register_callbacks as register_filters_callbacks
from src.callbacks.charts import register_callbacks as register_charts_callbacks

# Load the two separate DataFrames as global variables
df_locations, df_housing = load_data()

app = Dash(__name__, title="Canadian House Prices", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Pass both DataFrames to the layout
app.layout = create_layout(df_housing)

# Register callbacks, passing both DataFrames if needed
register_filters_callbacks(app)
register_charts_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)