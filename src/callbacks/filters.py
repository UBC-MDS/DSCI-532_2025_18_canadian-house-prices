from dash import Input, Output
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.data_loader import load_data

df = load_data()

def register_filter_callbacks(app):
    @app.callback(
        Output("city-filter", "options"),
        Input("province-filter", "value")
    )
    def update_city_options(selected_provinces):
        filtered_df = df[df["Province"].isin(selected_provinces)] if selected_provinces else df
        return [{"label": city, "value": city} for city in filtered_df["City"].unique()]
