#to get the tickers and fetch the raw stock data

import pandas as pd
import yfinance as yf

def get_sp500_tickers():
    """
    Sources S&P500 tickers from wikipedia.
    Returns a list of ticker symbols.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url)[0]
    return table['Symbol'].str.replace('.', '-', regex=False).tolist()


def download_stock_data(tickers, end=None):
    """
    Downloads the full available historical stock price data
    from companies currently listed in S&P500 using yfinance.

    Returns:
        Combined DataFrame of all stocks
    """
    all_data = []
    for ticker in tickers:
        try:
            print(f"Downloading {ticker}...")
            df = yf.download(ticker, end=end)
            if not df.empty:
                df['Ticker'] = ticker
                all_data.append(df.reset_index())
            else:
                print(f"No data found for {ticker}")
        except Exception as e:
            print(f"Failed to fetch data for {ticker}: {e}")
    return pd.concat(all_data, ignore_index=True)

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        print("⚠️ No valid data was downloaded.")
        return pd.DataFrame()  # return an empty DataFrame instead of crashing
