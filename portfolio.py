import sqlite3
import pandas as pd
import numpy as np

# Load data
conn = sqlite3.connect("data/cac40_prices.sqlite")
df = pd.read_sql("SELECT date, ticker, close FROM stock_prices", conn)
conn.close()

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Pivot to time series format
df_pivot = df.pivot(index="date", columns="ticker", values="close").dropna(axis=1)

# Log returns
log_returns = np.log(df_pivot / df_pivot.shift(1)).dropna()

# Annualized metrics
mean_returns = log_returns.mean() * 252
volatility = log_returns.std() * np.sqrt(252)
sharpe_ratios = mean_returns / volatility

# Create summary DataFrame
summary_df = pd.DataFrame({
    "Annualized Return": mean_returns,
    "Annualized Volatility": volatility,
    "Sharpe Ratio": sharpe_ratios
})

print(summary_df.sort_values("Sharpe Ratio", ascending=False))

def generate_random_portfolios(returns, num_portfolios=20000):
    num_assets = returns.shape[1]
    weights = np.random.dirichlet(np.ones(num_assets), size=num_portfolios)

    port_returns = []
    port_vols = []
    sharpe_ratios = []

    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252

    for w in weights:
        ret = np.dot(w, mean_returns)
        vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
        sharpe = ret / vol

        port_returns.append(ret)
        port_vols.append(vol)
        sharpe_ratios.append(sharpe)

    return weights, np.array(port_returns), np.array(port_vols), np.array(sharpe_ratios)
