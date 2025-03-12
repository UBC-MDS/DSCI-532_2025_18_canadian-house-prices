import pandas as pd

_data = None

def load_data():
    global _data
    if _data is None:

        file_path = r"data/processed/Cleaned_CanadianHousePrices.feather"
        # _data = pd.read_csv(file_path, encoding='ISO-8859-1').dropna()
        _data = pd.read_feather(file_path).dropna()
    return _data