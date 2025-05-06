#to get the tickers and fetch the raw stock data
import pandas as pd

def get_local_stock_data(path="data/CAC40_stocks_2021_2023.csv"):
    """
    Loads stock data from a local CSV file.
    This replaces the extract step from an online API.
    """
    try:
        df = pd.read_csv(path)
        print(f"Successfully loaded data from {path}")
        return df
    except FileNotFoundError:
        print(f"File not found: {path}")
        return pd.DataFrame()
