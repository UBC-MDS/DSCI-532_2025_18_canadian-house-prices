import pandas as pd

_data = None

def load_data():

    print("load_data called from data_loader.py")
    global _data
    if _data is None:
        file_path = r"data/processed/Cleaned_CanadianHousePrices.feather"
        print("reading data from data_loader.py")

        _data = pd.read_feather(file_path).dropna()
    return _data