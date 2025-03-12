import pandas as pd

def load_data():
    file_path = r"data/processed/Cleaned_CanadianHousePrices.feather"
    # df = pd.read_csv(file_path, encoding='ISO-8859-1').dropna()
    df = pd.read_feather(file_path).dropna()
    return df