#%%

import pandas as pd

def clean_stock_data(df):
    """
    Cleans and formats stock data:
    - Drops missing values
    - Standardizes column names to lowercase with underscores
    - Ensures 'date' column is datetime type
    """
    df = df.dropna()
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    return df