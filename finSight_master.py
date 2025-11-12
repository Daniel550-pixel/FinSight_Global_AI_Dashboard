import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf
import requests

INITIAL_INVESTMENT = 25000
CURRENCIES = USD EUR GBP JPY CHF
FALLBACK_RATES = {"EUR":1.1,"GBP":1.3,"JPY":0.007,"CHF":1.05}

def get_forex_rate(currency):
    try:
        r = requests.get(f"https://api.exchangerate.host/latest?base=USD&symbols={currency}")
        return r.json()["rates"][currency]
    except:
        return FALLBACK_RATES.get(currency,1)

def monte_carlo_simulation(initial, mu=0.15, sigma=0.25, years=50, simulations=500):
    results=[]
    for _ in range(simulations):
        w=initial
        path=[w]
        for _ in range(years):
            w *= np.random.normal(1+mu,sigma)
            path.append(w)
        results.append(path)
    return np.array(results)

st.title("FinSight Global AI Dashboard")
initial_investment = st.sidebar.number_input("Initial Investment (€)", value=INITIAL_INVESTMENT)
years_to_simulate = st.sidebar.slider("Years to Forecast", 1, 50, 30)
currency = st.sidebar.selectbox("Currency", CURRENCIES)

rate = get_forex_rate(currency)
adjusted_investment = initial_investment * rate
st.write(f"Investment in {currency}: {adjusted_investment:,.2f}")

st.subheader("Monte Carlo Wealth Simulation")
mc = monte_carlo_simulation(adjusted_investment, years=years_to_simulate)
median = np.median(mc,axis=0)
fig = px.line(y=median, labels={"x":"Year","y":"Net Worth"})
st.plotly_chart(fig)

st.subheader("ARR/MRR Projections")
ARR = adjusted_investment*0.15
MRR = ARR/12
st.write(f"Projected ARR: {ARR:,.2f} {currency}")
st.write(f"Projected MRR: {MRR:,.2f} {currency}")
