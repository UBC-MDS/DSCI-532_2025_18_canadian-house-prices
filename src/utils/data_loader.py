import pandas as pd

# Define global variables for the two datasets
_data_locations = None
_data_housing = None

def load_data():
    """
    Load and merge the location and housing datasets into a single DataFrame.
    
    Returns:
        pd.DataFrame: Merged DataFrame containing all data.
    """
    print("load_data called from data_loader.py")
    global _data_locations, _data_housing, _data

    # Load locations dataset if not already loaded
    if _data_locations is None:
        file_path_locations = r"data/processed/locations.feather"
        print("reading locations data from data_loader.py")
        _data_locations = pd.read_feather(file_path_locations)

    # Load housing dataset if not already loaded
    if _data_housing is None:
        file_path_housing = r"data/processed/housing_data.feather"
        print("reading housing data from data_loader.py")
        _data_housing = pd.read_feather(file_path_housing)

    return _data_locations, _data_housing