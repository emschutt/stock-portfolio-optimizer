#%%

import pandas as pd

def clean_stock_data(df):
    """
    Cleans and formats stock data:
    - Drops missing values
    - Renames columns to standardized format
    - Ensures 'date' column is datetime type
    """
    df = df.dropna()

    # Rename columns for consistency
    df = df.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume",
        "Stock": "ticker"
    })

    # Make sure date is datetime type
    df['date'] = pd.to_datetime(df['date'])

    return df
