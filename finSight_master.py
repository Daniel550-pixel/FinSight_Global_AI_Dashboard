import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="FinSight Global",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# FinSight Global — UI foundation
# This first interface is intentionally data-safe: all displayed market values
# are clearly labelled as demo/simulation data until real data providers exist.
# -----------------------------------------------------------------------------

st.markdown(
    """
    <style>
    :root { color-scheme: dark; }
    .stApp { background: #07090d; }
    [data-testid="stSidebar"] { background: #0a0d12; border-right: 1px solid #1c222c; }
    [data-testid="stSidebar"] * { color: #d9e0e8; }
    .block-container { padding: 1.6rem 2.2rem 3rem; max-width: 1700px; }
    h1, h2, h3 { letter-spacing: -0.025em; }
    h1 { font-size: 2.15rem !important; margin-bottom: .15rem !important; }
    .eyebrow { color: #718096; font-size: .72rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
    .subtle { color: #7f8b99; font-size: .86rem; }
    .status { display:inline-flex; align-items:center; gap:.45rem; padding:.28rem .65rem; border:1px solid #26303d; border-radius:999px; background:#0d1219; color:#aeb8c5; font-size:.75rem; }
    .dot { width:7px; height:7px; border-radius:50%; background:#4ade80; display:inline-block; }
    .card { background:linear-gradient(145deg,#0d1117,#0a0d12); border:1px solid #1b232e; border-radius:14px; padding:1rem 1.05rem; }
    .signal { border-left:3px solid #7dd3fc; padding:.7rem .85rem; background:#0c1118; border-radius:0 10px 10px 0; margin:.45rem 0; }
    .signal strong { color:#eef4fa; }
    .signal span { color:#8793a2; font-size:.8rem; }
    .risk-high { color:#fb7185; }
    .risk-med { color:#fbbf24; }
    .risk-low { color:#4ade80; }
    div[data-testid="stMetric"] { background:#0c1016; border:1px solid #1b232e; padding:.75rem .85rem; border-radius:12px; }
    div[data-testid="stMetricLabel"] { color:#7f8b99; }
    div[data-testid="stMetricValue"] { color:#eef4fa; }
    button[kind="secondary"] { border-color:#26303d; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------- Demo dataset --------------------------------
rng = np.random.default_rng(42)
dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=120, freq="D")
returns = rng.normal(0.0007, 0.012, len(dates))
portfolio = 100_000 * np.cumprod(1 + returns)
benchmark = 100_000 * np.cumprod(1 + rng.normal(0.00045, 0.0105, len(dates)))
performance = pd.DataFrame({"Portfolio": portfolio, "Benchmark": benchmark}, index=dates)

assets = pd.DataFrame(
    {
        "Asset": ["S&P 500", "Nasdaq 100", "Bitcoin", "Gold", "Brent Crude", "EUR/USD"],
        "Price": [6481.2, 23914.6, 113420.0, 3812.4, 68.7, 1.174],
        "1D": [0.82, 1.34, -0.74, 0.41, -1.18, 0.22],
        "Signal": ["Bullish", "Bullish", "Neutral", "Bullish", "Bearish", "Neutral"],
    }
)

# ------------------------------- Sidebar -------------------------------------
with st.sidebar:
    st.markdown("# ◈ FinSight")
    st.markdown('<div class="subtle">GLOBAL INTELLIGENCE TERMINAL</div>', unsafe_allow_html=True)
    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "Overview",
            "Markets",
            "Portfolio",
            "Intelligence",
            "Risk",
            "Strategies",
            "Backtesting",
            "Execution",
            "Alerts",
        ],
        label_visibility="visible",
    )

    st.divider()
    st.markdown('<div class="eyebrow">Environment</div>', unsafe_allow_html=True)
    st.markdown('<span class="status"><span class="dot"></span> PAPER / SIMULATION</span>', unsafe_allow_html=True)
    st.caption("Live providers are not connected yet.")
    st.divider()
    st.caption("FinSight Global · UI Foundation v0.1")

# ------------------------------- Header --------------------------------------
st.markdown('<div class="eyebrow">FINANCIAL INTELLIGENCE PLATFORM</div>', unsafe_allow_html=True)
st.title(page)
st.markdown(
    '<span class="status"><span class="dot"></span> SYSTEM ONLINE</span> '
    '<span class="subtle"> · Demo data layer · Architecture under reconstruction</span>',
    unsafe_allow_html=True,
)
st.write("")

# -------------------------------- Overview ------------------------------------
if page == "Overview":
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Portfolio Value", "$104,284", "+4.28%")
    c2.metric("Today", "+$1,482", "+1.44%")
    c3.metric("Risk Score", "32 / 100", "Low")
    c4.metric("Available Cash", "$18,640", "17.9%")

    st.write("")
    left, right = st.columns([2.1, 1])
    with left:
        st.markdown("### Portfolio intelligence")
        st.caption("Indexed performance · 120-day demonstration series")
        st.line_chart(performance, height=330, use_container_width=True)

    with right:
        st.markdown("### AI signal feed")
        st.markdown('<div class="signal"><strong>Risk regime</strong><br><span>Low-to-moderate volatility regime detected.</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="signal"><strong>Equity momentum</strong><br><span>Broad-market momentum remains positive.</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="signal"><strong>Concentration</strong><br><span>Technology exposure is above neutral.</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="signal"><strong>Macro watch</strong><br><span>Rates and energy remain key risk drivers.</span></div>', unsafe_allow_html=True)

    st.write("")
    a, b, c = st.columns(3)
    with a:
        st.markdown("### Allocation")
        st.bar_chart(pd.Series({"Equities": 48, "Crypto": 17, "Fixed income": 15, "Commodities": 10, "Cash": 10}), height=220)
    with b:
        st.markdown("### Risk factors")
        st.dataframe(pd.DataFrame({"Factor": ["Volatility", "Concentration", "Liquidity", "Drawdown"], "Score": [28, 44, 16, 22], "State": ["Low", "Medium", "Low", "Low"]}), hide_index=True, use_container_width=True)
    with c:
        st.markdown("### System roadmap")
        for item in ["UI foundation", "Data ingestion", "Analytics engine", "AI reasoning", "Execution controls"]:
            st.markdown(f"• {item}")

# -------------------------------- Markets -------------------------------------
elif page == "Markets":
    st.markdown("### Global market monitor")
    st.caption("Demonstration values only — real-time market feeds will be connected later.")
    st.dataframe(assets, hide_index=True, use_container_width=True)
    st.write("")
    x, y = st.columns([1.5, 1])
    with x:
        st.markdown("### Market breadth")
        breadth = pd.Series({"Advancing": 61, "Neutral": 18, "Declining": 21})
        st.bar_chart(breadth, height=260)
    with y:
        st.markdown("### Global regime")
        st.metric("Regime", "Risk-On", "Moderate confidence")
        st.metric("Volatility", "18.4", "Normal")
        st.metric("Liquidity", "Healthy", "Stable")

# -------------------------------- Portfolio -----------------------------------
elif page == "Portfolio":
    st.markdown("### Portfolio command center")
    c1, c2, c3 = st.columns(3)
    c1.metric("Net Liquidation", "$104,284", "+4.28%")
    c2.metric("Max Drawdown", "-6.8%", "Current cycle")
    c3.metric("Sharpe Ratio", "1.42", "Demo calculation")
    st.write("")
    holdings = pd.DataFrame({
        "Position": ["US Equities", "Technology", "Bitcoin", "Gold", "Cash"],
        "Weight": [31.0, 17.0, 17.0, 10.0, 25.0],
        "P/L": [8.4, 11.2, 3.1, 5.7, 0.0],
        "Risk": ["Medium", "High", "High", "Low", "Low"],
    })
    st.dataframe(holdings, hide_index=True, use_container_width=True)
    st.markdown("### Portfolio trajectory")
    st.line_chart(performance, height=340, use_container_width=True)

# ------------------------------- Intelligence --------------------------------
elif page == "Intelligence":
    st.markdown("### FinSight intelligence layer")
    st.caption("The future AI layer will combine market data, portfolio state, research, models and risk constraints.")
    q = st.text_input("Ask FinSight", placeholder="e.g. Why is portfolio risk increasing?")
    if q:
        st.info("Demo response: the reasoning layer is not connected yet. This workspace is ready for the intelligence engine.")
    st.write("")
    cols = st.columns(3)
    cards = [
        ("Market Intelligence", "Regimes, momentum, macro, breadth and cross-asset relationships."),
        ("Research Intelligence", "Company, asset, sector and event-level analysis."),
        ("Portfolio Intelligence", "Allocation, performance, exposures, attribution and optimization."),
    ]
    for col, (title, body) in zip(cols, cards):
        with col:
            st.markdown(f'<div class="card"><h4>{title}</h4><span class="subtle">{body}</span></div>', unsafe_allow_html=True)

# ----------------------------------- Risk -------------------------------------
elif page == "Risk":
    st.markdown("### Risk command center")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Risk", "32", "Low")
    c2.metric("VaR 95%", "$3,180", "1-day demo")
    c3.metric("CVaR 95%", "$4,760", "1-day demo")
    c4.metric("Stress Loss", "-$8,420", "Scenario")
    st.write("")
    risk = pd.DataFrame({"Risk Domain": ["Market", "Concentration", "Liquidity", "Volatility", "Counterparty"], "Score": [31, 44, 16, 28, 8], "Status": ["Low", "Medium", "Low", "Low", "Low"]})
    st.dataframe(risk, hide_index=True, use_container_width=True)
    st.markdown("### Scenario monitor")
    st.bar_chart(pd.Series({"Rates +100bp": -4.2, "Equities -10%": -6.8, "Crypto -25%": -4.1, "Oil +20%": 0.7}), height=280)

# -------------------------------- Strategies ----------------------------------
elif page == "Strategies":
    st.markdown("### Strategy laboratory")
    strategies = pd.DataFrame({
        "Strategy": ["Global Momentum", "Risk Parity", "Trend + Macro", "Adaptive Allocation"],
        "Status": ["Ready for data", "Design", "Design", "Research"],
        "Target Vol": ["12%", "10%", "14%", "Dynamic"],
        "Execution": ["Paper", "Paper", "Paper", "Paper"],
    })
    st.dataframe(strategies, hide_index=True, use_container_width=True)
    st.write("")
    st.markdown("### Strategy builder")
    a, b, c = st.columns(3)
    with a: st.selectbox("Signal family", ["Momentum", "Mean Reversion", "Macro", "Multi-Factor"])
    with b: st.selectbox("Risk model", ["Volatility Target", "Risk Parity", "Fixed Risk", "Adaptive"])
    with c: st.selectbox("Execution mode", ["Paper", "Backtest", "Simulation"])
    st.button("Build strategy specification")

# -------------------------------- Backtesting ---------------------------------
elif page == "Backtesting":
    st.markdown("### Backtesting laboratory")
    st.caption("Historical data, execution costs and strategy logic will be wired into this workspace next.")
    c1, c2, c3 = st.columns(3)
    c1.metric("CAGR", "14.8%", "Demo")
    c2.metric("Sharpe", "1.31", "Demo")
    c3.metric("Max Drawdown", "-11.4%", "Demo")
    st.line_chart(performance, height=350, use_container_width=True)

# -------------------------------- Execution -----------------------------------
elif page == "Execution":
    st.markdown("### Execution control room")
    st.warning("PAPER / SIMULATION ONLY — no live orders can be submitted from this UI.")
    orders = pd.DataFrame({"Time": ["09:42", "10:18", "11:07"], "Asset": ["SPY", "BTC", "GLD"], "Side": ["BUY", "BUY", "SELL"], "Qty": [12, 0.025, 8], "Status": ["Simulated", "Simulated", "Simulated"]})
    st.dataframe(orders, hide_index=True, use_container_width=True)
    st.markdown("### Order staging")
    a, b, c = st.columns(3)
    with a: st.text_input("Asset", "SPY")
    with b: st.number_input("Quantity", min_value=0.0, value=1.0)
    with c: st.selectbox("Side", ["BUY", "SELL"])
    st.button("Stage paper order")

# ---------------------------------- Alerts ------------------------------------
else:
    st.markdown("### Alert center")
    alerts = pd.DataFrame({
        "Severity": ["Medium", "Low", "Low", "Info"],
        "Alert": ["Technology concentration above target", "Gold momentum improving", "Volatility normalizing", "Portfolio rebalance window approaching"],
        "State": ["Open", "Open", "Acknowledged", "Open"],
    })
    st.dataframe(alerts, hide_index=True, use_container_width=True)
    st.markdown("### Alert rules")
    st.checkbox("Drawdown threshold", value=True)
    st.checkbox("Volatility regime change", value=True)
    st.checkbox("Concentration threshold", value=True)
    st.checkbox("AI anomaly detection", value=False)

st.divider()
st.caption("FinSight Global · UI foundation · Demo/simulation data only")
