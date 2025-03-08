from dash import Output, Input
from src.utils.data_loader import load_data

df = load_data()

def register_callbacks(app):
    # Callback for updating city options based on selected provinces
    @app.callback(
        Output("city-filter", "options"),
        Input("province-filter", "value")
    )
    def update_city_options(selected_provinces):
        if selected_provinces and len(selected_provinces) > 0:
            filtered_df = df[df["Province"].isin(selected_provinces)]
            city_options = [{"label": city, "value": city} for city in filtered_df["City"].unique()]
        else:
            city_options = [{"label": city, "value": city} for city in df["City"].unique()]
        return city_options

    # Callback to reset the filters to default values
    @app.callback(
        [Output("city-filter", "value"),
         Output("province-filter", "value"),
         Output("bedrooms-slider", "value"),
         Output("bathrooms-slider", "value")],
        Input("reset-button", "n_clicks"),
        prevent_initial_call=True
    )
    def reset_filters(n_clicks):
        return (
            ["Vancouver", "Toronto", "Montreal", "Ottawa"],
            [],  # Province filter is reset to empty (or default values if you prefer)
            [df["Number_Beds"].min(), df["Number_Beds"].max()],
            [df["Number_Baths"].min(), df["Number_Baths"].max()]
        )

   