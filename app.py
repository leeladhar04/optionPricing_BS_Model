import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from black_scholes import black_scholes
from greeks import delta, gamma
import seaborn as sns 

st.title("Option Pricing Visualization using Black-Scholes Model")


st.sidebar.header("Input Parameters")
S = st.sidebar.slider("Spot Price (S)", 50.0, 150.0, 100.0)
K = st.sidebar.slider("Strike Price (K)", 50.0, 150.0, 100.0)
T = st.sidebar.slider("Time to Maturity (T in years)", 0.1, 2.0, 1.0)
r = st.sidebar.slider("Risk-Free Rate (r)", 0.0, 0.2, 0.05)
sigma = st.sidebar.slider("Volatility (σ)", 0.1, 0.5, 0.2)
option_type = st.sidebar.radio("Option Type", ["call", "put"])


price = black_scholes(S, K, T, r, sigma, option_type)
st.write(f"The {option_type.capitalize()} Option Price: **${price:.2f}**")

delta_val = delta(S, K, T, r, sigma, option_type)
gamma_val = gamma(S, K, T, r, sigma)
st.write(f"Delta: **{delta_val:.2f}**, Gamma: **{gamma_val:.2f}**")

st.subheader("Option Price vs Spot Price")
S_range = np.linspace(50, 150, 100)
prices = [black_scholes(s, K, T, r, sigma, option_type) for s in S_range]
plt.figure(figsize=(10, 6))
plt.plot(S_range, prices, label=f"{option_type.capitalize()} Option Price")
plt.title("Option Price vs Spot Price")
plt.xlabel("Spot Price (S)")
plt.ylabel("Option Price")
plt.legend()
st.pyplot(plt)


st.subheader("3D Surface Plot: Option Price")
S = np.linspace(50, 150, 50)
sigma = np.linspace(0.1, 0.5, 50)
S, sigma = np.meshgrid(S, sigma)
prices_3d = np.vectorize(black_scholes)(S, K, T, r, sigma, option_type)

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(S, sigma, prices_3d, cmap='viridis')
ax.set_title(f"{option_type.capitalize()} Option Price Surface")
ax.set_xlabel("Spot Price (S)")
ax.set_ylabel("Volatility (σ)")
ax.set_zlabel("Option Price")
st.pyplot(fig)


st.subheader("Heatmap: Option Price Sensitivity")

S_range = np.linspace(50, 150, 50)
sigma_range = np.linspace(0.1, 0.5, 50)
S_grid, sigma_grid = np.meshgrid(S_range, sigma_range)
prices_grid = np.vectorize(black_scholes)(S_grid, K, T, r, sigma_grid, option_type)


fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(prices_grid, ax=ax, cmap="coolwarm", cbar_kws={'label': 'Option Price'})
ax.set_title(f"Option Price Heatmap ({option_type.capitalize()})")
ax.set_xlabel("Spot Price (S)")
ax.set_ylabel("Volatility (σ)")
ax.set_xticks(np.linspace(0, len(S_range) - 1, 5))
ax.set_xticklabels(np.linspace(S_range.min(), S_range.max(), 5).astype(int))
ax.set_yticks(np.linspace(0, len(sigma_range) - 1, 5))
ax.set_yticklabels(np.round(np.linspace(sigma_range.min(), sigma_range.max(), 5), 2))
st.pyplot(fig)
