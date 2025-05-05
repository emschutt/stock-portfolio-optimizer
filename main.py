from etl.extract import get_sp500_tickers, download_stock_data
from etl.transform import clean_stock_data
from etl.load import save_to_sqlite
from datetime import datetime

if __name__ == "__main__":
    # Get list of S&P 500 tickers
    tickers = get_sp500_tickers()
    print(f"Fetched {len(tickers)} tickers")

    # Sample for testing (use full list when ready)
    sample_tickers = tickers[:50]

    # Download data (from earliest available date to today)
    raw_data = download_stock_data(sample_tickers)
    if raw_data.empty:
        print("❌ No data to clean or save. Exiting program.")
        exit()

    # Clean the data
    clean_data = clean_stock_data(raw_data)

    # Save to SQLite database
    save_to_sqlite(clean_data)

    print("✅ ETL pipeline completed! Data saved to database.")

# Preview the data saved to the database
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/sp500_prices.sqlite")
df = pd.read_sql("SELECT * FROM stock_prices LIMIT 5", conn)
print(df.head())
conn.close()