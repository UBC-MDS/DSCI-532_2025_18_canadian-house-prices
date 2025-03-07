import pandas as pd
import os
import sys

# Ensure the module can be imported regardless of execution location
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Construct absolute path to the data file
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # Get project root
FILE_PATH = os.path.join(BASE_DIR, "data", "processed", "Cleaned_CanadianHousePrices.csv")

def load_data():
    """Load and preprocess the dataset."""
    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError(f"Data file not found: {FILE_PATH}")

    df = pd.read_csv(FILE_PATH, encoding="ISO-8859-1").dropna()
    return df
