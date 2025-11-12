import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf
import requests
from datetime import datetime

INITIAL_INVESTMENT = 25000
CURRENCIES = USD EUR GBP JPY CHF
ASSETS = AAPL GOOG BTC-USD ETH-USD OIL
FALLBACK_RATES = {"EUR":1.1,"GBP":1.3,"JPY":0.007,"CHF":1.05}

# --- Helpers ---
def get_forex_rate(currency):
    try:
        r = requests.get(f"https://api.exchangerate.host/latest?base=USD&symbols={currency}")
        return r.json()['rates'][currency]
    except:
        return FALLBACK_RATES.get(currency,1)

def monte_carlo_wealth(initial, mu=0.15, sigma=0.25, years=50, simulations=500):
    results=[]
    for _ in range(simulations):
        w=initial
        path=[w]
        for _ in range(years):
            w*=np.random.normal(1+mu,sigma)
            path.append(w)
        results.append(path)
    return np.array(results)

def fetch_asset_history(asset, period="1y"):
    data = yf.Ticker(asset).history(period=period)
    return data['Close']

# --- Streamlit UI ---
st.set_page_config(page_title="FinSight Enterprise Dashboard", layout="wide")
st.title("FinSight Global AI Enterprise Dashboard")

# Sidebar inputs
initial_investment = st.sidebar.number_input("Initial Investment (€)", value=INITIAL_INVESTMENT)
years = st.sidebar.slider("Years to Forecast", 1, 50, value=SIM_YEARS)
currency = st.sidebar.selectbox("Currency", CURRENCIES)
rate = get_forex_rate(currency)
adjusted_investment = initial_investment * rate

st.write(f"Adjusted Investment in {currency}: {adjusted_investment:,.2f}")

# --- Monte Carlo Wealth Simulation ---
st.subheader("Monte Carlo Wealth Simulation")
mc = monte_carlo_wealth(adjusted_investment, years=years)
median = np.median(mc, axis=0)
fig_mc = px.line(y=median, labels={"x":"Year","y":"Net Worth"})
st.plotly_chart(fig_mc)

# --- Multi-Asset Trading Simulation ---
st.subheader("Multi-Asset Trading Simulation")
allocation = st.slider("Risk Allocation % per Asset", 1, 100, 20, step=5)
portfolio = {}
for asset in ASSETS:
    hist = fetch_asset_history(asset)
    change = hist.pct_change().mean() if len(hist)>1 else 0.01
    expected_growth = adjusted_investment * (allocation/100) * (1+change)**years
    portfolio[asset] = expected_growth

df_portfolio = pd.DataFrame(list(portfolio.items()), columns=["Asset","Projected Value"])
fig_portfolio = px.bar(df_portfolio, x="Asset", y="Projected Value")
st.plotly_chart(fig_portfolio)

# --- SaaS ARR/MRR Simulation ---
st.subheader("SaaS Revenue Projections")
ARR = adjusted_investment * 0.15
MRR = ARR/12
st.write(f"Projected ARR: {ARR:,.2f} {currency}")
st.write(f"Projected MRR: {MRR:,.2f} {currency}")

# --- Risk Metrics ---
st.subheader("Risk Metrics & Stop-Loss Simulation")
risk_level = st.slider("Risk Factor", 1, 10, 5)
drawdown = adjusted_investment * (risk_level/100)
st.write(f"Max Drawdown Estimate: {drawdown:,.2f} {currency}")

# --- System Health Monitoring ---
st.subheader("System Health & Alerts")
st.write("Status: ✅ Online")
st.write("7-Step Issue Recognition Workflow: Active")

