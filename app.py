# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from portfolio import df_pivot, generate_random_portfolios

# --- UI Controls ---
st.title("📊 Optimized Portfolio Builder")

risk_profile = st.selectbox("Select Risk Profile", ["Low", "Moderate", "High"])
max_return = st.radio("Optimization Objective", ["Maximize Sharpe Ratio", "Maximize Return"])

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

# --- Determine valid range for Num Stocks ---
min_stocks = max(1, int(filtered["Num Stocks"].min())) if not filtered.empty else 1
max_stocks = max(min_stocks, int(filtered["Num Stocks"].max())) if not filtered.empty else 37

# Clamp default within valid bounds
default_stocks = st.session_state.get("selected_stocks", max_stocks)
default_stocks = max(min_stocks, min(max_stocks, default_stocks))

selected_stocks = st.slider(
    "Max Number of Stocks",
    min_stocks,
    max_stocks,
    value=default_stocks,
    key="selected_stocks"
)

filtered = filtered[filtered["Num Stocks"] <= selected_stocks]

# --- Optimization Objective ---
if not filtered.empty:
    if max_return == "Maximize Return":
        best_idx = filtered["Return"].idxmax()
    else:
        best_idx = filtered["Sharpe Ratio"].idxmax()

    best_portfolio = filtered.loc[best_idx]

    # --- Display Best Portfolio ---
    st.subheader("Best Portfolio Weights")
    weights_df = best_portfolio[df_pivot.columns]
    weights_df = weights_df[weights_df > 0.01].sort_values(ascending=False)
    st.dataframe(weights_df)
    st.bar_chart(weights_df)

    # --- Display Stats ---
    st.metric("Expected Return", f"{best_portfolio['Return']:.2%}")
    st.metric("Volatility", f"{best_portfolio['Volatility']:.2%}")
    st.metric("Sharpe Ratio", f"{best_portfolio['Sharpe Ratio']:.2f}")

    # --- Backtest Performance Plot ---
    st.subheader("Simulated Backtest Performance")

    aligned_weights = weights_df.reindex(df_pivot.columns, fill_value=0.0)
    cum_returns = (returns @ aligned_weights).cumsum()
    base = cum_returns.iloc[0]
    normalized = (cum_returns - base + 1) * 100

    fig, ax = plt.subplots()
    ax.plot(normalized, label="Cumulative Return")
    ax.set_title("Backtested Portfolio Performance")
    ax.set_ylabel("Portfolio Value (Index)")
    ax.set_xlabel("Date")
    ax.legend()
    st.pyplot(fig)

else:
    st.warning("⚠️ No portfolios matched the selected criteria. Try adjusting risk or max stock number.")
