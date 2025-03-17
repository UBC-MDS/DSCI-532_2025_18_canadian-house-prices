from dash import Output, Input, State
from src.utils.data_loader import load_data

# Load the datasets once when the module is imported
df_locations, df_housing = load_data()

def register_callbacks(app):
    """
    Registers all Dash callbacks for interactive functionality.

    Args:
        app (Dash): The Dash application instance.

    Callbacks:
        - update_city_options: Updates the city dropdown options based on selected provinces.
        - reset_filters: Resets all filters to their default values.
        - toggle_about_text: Toggles the visibility of the About section.
    """
    # Callback for updating city options based on selected provinces
    @app.callback(
        Output("city-filter", "options"),
        Input("province-filter", "value")
    )
    def update_city_options(selected_provinces):
        """
        Updates the city filter dropdown options based on the selected provinces.

        Args:
            selected_provinces (list): A list of selected province names.

        Returns:
            list: A list of city options as dictionaries with "label" and "value".
        """
        if selected_provinces and len(selected_provinces) > 0:
            filtered_df = df_housing[df_housing["Province"].isin(selected_provinces)]
            city_options = [{"label": city, "value": city} for city in filtered_df["City"].unique()]
        else:
            city_options = [{"label": city, "value": city} for city in df_housing["City"].unique()]
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
        """
        Resets all filter inputs to their default values when the reset button is clicked.

        Args:
            n_clicks (int): The number of times the reset button has been clicked.

        Returns:
            tuple: Default values for city, province, bedroom slider, and bathroom slider.
        """
        return (
            ["Vancouver", "Toronto", "Montreal", "Ottawa"],
            [],  # Province filter is reset to empty (or default values if you prefer)
            [df_housing["Number_Beds"].min(), df_housing["Number_Beds"].max()],
            [df_housing["Number_Baths"].min(), df_housing["Number_Baths"].max()]
        )

    # Callback to toggle About text visibility
    @app.callback(
        Output("about-text", "style"),
        Input("about-button", "n_clicks"),
        State("about-text", "style"),
        prevent_initial_call=True  # Prevents callback from firing on page load
    )
    def toggle_about_text(n_clicks, current_style):
        """
        Toggles the visibility of the About section when the button is clicked.

        Args:
            n_clicks (int): The number of times the about button has been clicked.
            current_style (dict): The current CSS style of the about-text element.

        Returns:
            dict: The updated style dictionary to show or hide the text.
        """
        if n_clicks is None:
            return {"display": "none"}
        if current_style["display"] == "none":
            return {"display": "block"}  # Show the text
        return {"display": "none"}  # Hide the text again