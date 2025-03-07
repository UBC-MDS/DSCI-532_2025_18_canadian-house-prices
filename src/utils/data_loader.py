import pandas as pd
import os
import sys

# Get the absolute path to the project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Construct the absolute path to the dataset
FILE_PATH = os.path.join(BASE_DIR, "data", "processed", "Cleaned_CanadianHousePrices.csv")

def load_data():
    """Load and preprocess the dataset."""
    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError(f"Data file not found at: {FILE_PATH}")

    df = pd.read_csv(FILE_PATH, encoding="ISO-8859-1").dropna()
    return df
