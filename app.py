# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from portfolio import df_pivot, generate_random_portfolios

st.set_page_config(page_title="Portfolio Optimizer Dashboard", layout="wide")

# --- Sidebar Controls ---
st.sidebar.title("Portfolio Settings")
risk_profile = st.sidebar.selectbox("Select Risk Profile", ["Low", "Moderate", "High"])
objective = st.sidebar.radio("Optimization Objective", ["Maximize Sharpe Ratio", "Maximize Return"])

# --- Portfolio Simulation ---
returns = df_pivot.pct_change().dropna()
weights, port_returns, port_vols, sharpe_ratios = generate_random_portfolios(returns)

results_df = pd.DataFrame(weights, columns=df_pivot.columns)
results_df["Return"] = port_returns
results_df["Volatility"] = port_vols
results_df["Sharpe Ratio"] = sharpe_ratios
results_df["Num Stocks"] = (results_df > 0.01).sum(axis=1)

# --- Filter by Risk Profile ---
if risk_profile == "Low":
    filtered = results_df[results_df["Volatility"] < results_df["Volatility"].quantile(0.33)]
elif risk_profile == "Moderate":
    filtered = results_df[(results_df["Volatility"] >= results_df["Volatility"].quantile(0.33)) &
                          (results_df["Volatility"] <= results_df["Volatility"].quantile(0.66))]
else:
    filtered = results_df[results_df["Volatility"] > results_df["Volatility"].quantile(0.66)]

# --- Slider for number of stocks ---
min_stocks = max(1, int(filtered["Num Stocks"].min())) if not filtered.empty else 1
max_stocks = max(min_stocks, int(filtered["Num Stocks"].max())) if not filtered.empty else 37
selected_stocks = st.sidebar.slider("Max Number of Stocks", min_stocks, max_stocks, value=max_stocks)
filtered = filtered[filtered["Num Stocks"] <= selected_stocks]

# --- Optimize ---
if not filtered.empty:
    if objective == "Maximize Return":
        best_idx = filtered["Return"].idxmax()
    else:
        best_idx = filtered["Sharpe Ratio"].idxmax()

    best_portfolio = filtered.loc[best_idx]
    weights_df = best_portfolio[df_pivot.columns]
    weights_df = weights_df[weights_df > 0.01].sort_values(ascending=False)

    st.title("Portfolio Optimizer Dashboard")

    # --- Backtest Chart ---
    st.subheader("Backtested Portfolio Performance")
    aligned_weights = weights_df.reindex(df_pivot.columns, fill_value=0.0)
    cum_returns = (returns @ aligned_weights).cumsum()
    base = cum_returns.iloc[0]
    normalized_returns = (cum_returns - base + 1) * 100

    fig, ax = plt.subplots(figsize=(6, 2))
    ax.plot(normalized_returns, label="Cumulative Return", color="dodgerblue", linewidth=1.5)
    ax.set_title("Backtested Portfolio Performance", fontsize=10)
    ax.set_ylabel("Portfolio Value (Index)", fontsize=8)
    ax.set_xlabel("Date", fontsize=8)
    ax.tick_params(labelsize=6)
    ax.legend(fontsize=6, loc='upper left')
    st.pyplot(fig)

    # --- Bar Chart of Weights ---
    st.subheader("Portfolio Composition")
    st.bar_chart(weights_df)

    # --- Portfolio Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Expected Return", f"{best_portfolio['Return']:.2%}")
    col2.metric("Volatility", f"{best_portfolio['Volatility']:.2%}")
    col3.metric("Sharpe Ratio", f"{best_portfolio['Sharpe Ratio']:.2f}")

    # --- Show Dataframe ---
    st.subheader("Portfolio Weights Table")
    st.dataframe(weights_df)

else:
    st.warning("No portfolios matched the selected criteria. Try adjusting risk or max stock number.")
