#%%

import sqlite3
import os

def save_to_sqlite(df, db_path="data/cac40_prices.sqlite", table_name="stock_prices"):
    """
    Saves the cleaned stock data to a SQLite database.

    Parameters:
        df: DataFrame to save
        db_path: path to the .sqlite file
        table_name: name of the table in the database
    """
    # Ensure the folder exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to SQLite and save the DataFrame
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

    print(f"✅ Data saved to {db_path} (table: {table_name})")
