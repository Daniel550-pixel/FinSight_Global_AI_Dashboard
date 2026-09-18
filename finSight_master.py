import math
import html
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="FinSight Global",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# FinSight Global — Terminal UI v0.2
# Visual direction: institutional research/trading terminal.
# All figures in this UI are DEMONSTRATION DATA until providers are connected.
# -----------------------------------------------------------------------------

CSS = r"""
<style>
:root {
    color-scheme: dark;
    --bg: #05070b;
    --panel: #0a0e14;
    --panel-2: #0d1219;
    --panel-3: #101722;
    --line: #1a2330;
    --line-2: #243040;
    --text: #edf2f7;
    --muted: #7f8b9a;
    --muted-2: #596575;
    --cyan: #63d7ff;
    --cyan-2: #2bb8e8;
    --green: #43d17a;
    --red: #ff6176;
    --amber: #e9ad4b;
    --violet: #9f8bff;
}
html, body, [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.stApp {
    background:
        radial-gradient(circle at 85% 0%, rgba(50, 110, 160, .10), transparent 30%),
        radial-gradient(circle at 10% 100%, rgba(80, 60, 170, .07), transparent 28%),
        var(--bg);
}
.block-container {
    max-width: 1780px;
    padding: 1rem 1.4rem 3rem;
}
[data-testid="stSidebar"] {
    background: #070a0f;
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] > div:first-child {
    padding: 1rem .8rem;
}
[data-testid="stSidebar"] * {
    color: var(--text);
}
[data-testid="stSidebar"] hr {
    margin: .8rem 0;
    border-color: var(--line);
}
[data-testid="stSidebar"] .stRadio > label {
    color: var(--muted);
    font-size: .68rem;
    font-weight: 800;
    letter-spacing: .16em;
    text-transform: uppercase;
}
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: .18rem;
}
[data-testid="stSidebar"] [role="radio"] {
    border-radius: 8px;
    padding: .45rem .6rem;
}
[data-testid="stSidebar"] [role="radio"]:hover {
    background: #0f151d;
}
[data-testid="stSidebar"] [role="radio"][aria-checked="true"] {
    background: #101a24;
    border: 1px solid #1d3948;
}
[data-testid="stSidebar"] [role="radio"] p {
    font-size: .88rem;
}
section[data-testid="stSidebar"] button {
    border-color: var(--line-2);
}
h1, h2, h3, h4 {
    letter-spacing: -.03em;
}
h1 {
    font-size: 2rem !important;
    margin: 0 !important;
}
h2 {
    font-size: 1.25rem !important;
}
h3 {
    font-size: 1rem !important;
}
p {
    line-height: 1.45;
}
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #0c1118, #080c11);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: .8rem .9rem;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: .72rem !important;
    text-transform: uppercase;
    letter-spacing: .08em;
}
[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-size: 1.55rem !important;
}
[data-testid="stMetricDelta"] {
    font-size: .75rem !important;
}
.stButton > button {
    border: 1px solid var(--line-2);
    background: #0d131b;
    color: var(--text);
    border-radius: 8px;
}
.stButton > button:hover {
    border-color: #2f6074;
    color: #ffffff;
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 10px;
    overflow: hidden;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #090d13;
    border-color: var(--line-2);
}
[data-testid="stTabs"] button {
    color: var(--muted);
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--text);
}
hr {
    border-color: var(--line);
}
.smallcaps {
    color: var(--muted);
    font-size: .66rem;
    font-weight: 800;
    letter-spacing: .15em;
    text-transform: uppercase;
}
.muted {
    color: var(--muted);
}
.muted2 {
    color: var(--muted-2);
}
.terminal-title {
    font-size: .9rem;
    font-weight: 750;
    letter-spacing: -.01em;
    color: var(--text);
}
.app-mark {
    font-size: 1.25rem;
    font-weight: 900;
    letter-spacing: -.05em;
}
.topbar {
    border: 1px solid var(--line);
    background: rgba(10, 14, 20, .84);
    border-radius: 12px;
    padding: .65rem .8rem;
    margin-bottom: .85rem;
    backdrop-filter: blur(14px);
}
.topbar-grid {
    display: grid;
    grid-template-columns: 1.2fr 1fr 1fr 1fr auto;
    gap: .6rem;
    align-items: center;
}
.top-item {
    padding: .1rem .45rem;
    border-right: 1px solid var(--line);
}
.top-item:last-child { border-right: 0; }
.top-value {
    color: var(--text);
    font-size: .82rem;
    font-weight: 700;
}
.top-note {
    color: var(--muted);
    font-size: .67rem;
    margin-top: .08rem;
}
.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
    background: var(--green);
    box-shadow: 0 0 10px rgba(67, 209, 122, .55);
}
.pill {
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    border: 1px solid #263443;
    border-radius: 999px;
    padding: .25rem .55rem;
    color: #b7c3cf;
    background: #0c1219;
    font-size: .67rem;
    font-weight: 750;
    letter-spacing: .06em;
    text-transform: uppercase;
}
.pill.green { color: #8ef0b0; border-color: #1f5134; background: #0c1811; }
.pill.amber { color: #f3c86e; border-color: #5d451f; background: #191309; }
.pill.red { color: #ff96a4; border-color: #5b2630; background: #190b0e; }
.panel {
    background: linear-gradient(155deg, rgba(14,19,27,.98), rgba(8,12,17,.98));
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: .9rem;
}
.panel-tight {
    background: #0a0f15;
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: .7rem;
}
.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: .7rem;
}
.panel-title {
    font-size: .92rem;
    font-weight: 800;
    color: var(--text);
}
.panel-subtitle {
    color: var(--muted);
    font-size: .68rem;
}
.kpi-big {
    font-size: 1.55rem;
    font-weight: 800;
    color: var(--text);
}
.kpi-change.up { color: var(--green); }
.kpi-change.down { color: var(--red); }
.kpi-change.flat { color: var(--muted); }
.feed {
    padding: .7rem 0;
    border-top: 1px solid var(--line);
}
.feed:first-child { border-top: 0; padding-top: 0; }
.feed-title {
    color: var(--text);
    font-size: .8rem;
    font-weight: 750;
}
.feed-body {
    color: var(--muted);
    font-size: .72rem;
    line-height: 1.45;
    margin-top: .15rem;
}
.feed-meta {
    color: var(--muted-2);
    font-size: .64rem;
    margin-top: .3rem;
}
.signal-bar {
    height: 5px;
    border-radius: 4px;
    background: #141c25;
    overflow: hidden;
    margin-top: .35rem;
}
.signal-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #2bb8e8, #8ddfff);
}
.watch-row {
    display: grid;
    grid-template-columns: 1.15fr .9fr .7fr .6fr;
    gap: .4rem;
    align-items: center;
    padding: .52rem .05rem;
    border-top: 1px solid var(--line);
    font-size: .73rem;
}
.watch-row.head {
    color: var(--muted-2);
    font-size: .62rem;
    letter-spacing: .08em;
    text-transform: uppercase;
    border-top: 0;
}
.num { text-align: right; font-variant-numeric: tabular-nums; }
.up { color: var(--green); }
.down { color: var(--red); }
.flat { color: var(--muted); }
.section-gap { height: .45rem; }
.workspace-strip {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: .15rem 0 .75rem;
}
.quote {
    color: var(--cyan);
    font-size: .75rem;
    font-weight: 700;
}
.ai-box {
    border: 1px solid #263247;
    background:
        radial-gradient(circle at 88% 16%, rgba(117, 102, 255, .18), transparent 28%),
        linear-gradient(150deg, #111527, #0a0f18);
    border-radius: 12px;
    padding: .9rem;
}
.ai-title {
    color: #c9c3ff;
    font-size: .68rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
}
.ai-headline {
    margin-top: .2rem;
    color: #f1efff;
    font-size: 1rem;
    font-weight: 800;
}
.ai-body {
    margin-top: .35rem;
    color: #9ca3b8;
    font-size: .73rem;
    line-height: 1.5;
}
.mini-tag {
    display: inline-block;
    padding: .16rem .4rem;
    margin-right: .25rem;
    border: 1px solid #293343;
    border-radius: 5px;
    color: #9aa8b8;
    background: #0c121a;
    font-size: .62rem;
}
.matrix-cell {
    padding: .55rem;
    border: 1px solid var(--line);
    background: #0a0f15;
    border-radius: 8px;
    min-height: 74px;
}
.matrix-name { font-size: .68rem; color: var(--muted); }
.matrix-value { font-size: 1rem; font-weight: 800; margin-top: .2rem; }
.hero {
    padding: .35rem 0 .8rem;
}
.hero h1 {
    font-size: 2.3rem !important;
}
div[data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Data helpers
# -----------------------------------------------------------------------------

def sparkline(values, width=180, height=40, stroke="#63d7ff"):
    arr = np.asarray(values, dtype=float)
    if len(arr) < 2:
        return ""
    mn, mx = float(arr.min()), float(arr.max())
    span = mx - mn if mx != mn else 1.0
    pts = []
    for i, value in enumerate(arr):
        x = i * (width - 4) / (len(arr) - 1) + 2
        y = height - 3 - ((value - mn) / span) * (height - 8)
        pts.append(f"{x:.1f},{y:.1f}")
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'<polyline fill="none" stroke="{stroke}" stroke-width="1.7" '
        f'stroke-linecap="round" stroke-linejoin="round" points="{" ".join(pts)}"/>'
        f'</svg>'
    )


def html_card(title, body, cls="panel"):
    return f'<div class="{cls}"><div class="panel-title">{html.escape(title)}</div>{body}</div>'


rng = np.random.default_rng(17)
dates = pd.date_range(end=pd.Timestamp.now().normalize(), periods=180, freq="D")
portfolio_returns = rng.normal(0.00062, 0.0115, len(dates))
benchmark_returns = rng.normal(0.00051, 0.0104, len(dates))
portfolio_curve = 100_000 * np.cumprod(1 + portfolio_returns)
benchmark_curve = 100_000 * np.cumprod(1 + benchmark_returns)

performance = pd.DataFrame(
    {"FinSight Portfolio": portfolio_curve, "Benchmark": benchmark_curve},
    index=dates,
)

assets = pd.DataFrame(
    {
        "Symbol": ["SPX", "NDX", "BTC", "GOLD", "BRENT", "EURUSD"],
        "Instrument": [
            "S&P 500", "Nasdaq 100", "Bitcoin", "Gold", "Brent Crude", "Euro / U.S. Dollar"
        ],
        "Price": [6481.2, 23914.6, 113420.0, 3812.4, 68.7, 1.174],
        "1D": [0.82, 1.34, -0.74, 0.41, -1.18, 0.22],
        "Signal": ["BULLISH", "BULLISH", "NEUTRAL", "BULLISH", "BEARISH", "NEUTRAL"],
        "Vol": [14.2, 17.8, 48.1, 16.7, 29.3, 7.9],
    }
)

holdings = pd.DataFrame(
    {
        "Symbol": ["VOO", "QQQ", "BTC", "GLD", "TLT", "CASH"],
        "Position": ["U.S. Equities", "Technology", "Bitcoin", "Gold", "Treasuries", "Cash"],
        "Weight": [27.5, 17.0, 14.5, 8.5, 7.5, 25.0],
        "P/L": [8.4, 11.2, 3.1, 5.7, 1.8, 0.0],
        "Risk": ["MED", "HIGH", "HIGH", "LOW", "LOW", "LOW"],
    }
)

news = [
    ("Macro", "Rates remain the primary cross-asset sensitivity.", "12 min ago"),
    ("Equities", "Technology leadership remains positive but concentrated.", "24 min ago"),
    ("Crypto", "Bitcoin volatility remains materially above major equity indices.", "39 min ago"),
    ("Commodities", "Energy weakness is pressuring the near-term inflation impulse.", "51 min ago"),
]


# -----------------------------------------------------------------------------
# Navigation
# -----------------------------------------------------------------------------

NAV = [
    "Overview",
    "Markets",
    "Portfolio",
    "Intelligence",
    "Risk",
    "Strategies",
    "Backtesting",
    "Execution",
    "Alerts",
]

with st.sidebar:
    st.markdown('<div class="app-mark">◈ FINSIGHT</div>', unsafe_allow_html=True)
    st.markdown('<div class="smallcaps">GLOBAL INTELLIGENCE TERMINAL</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    page = st.radio("WORKSPACE", NAV, index=0)

    st.divider()
    st.markdown('<div class="smallcaps">Terminal</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="margin-top:.45rem"><span class="pill green">'
        '<span class="status-dot"></span> PAPER MODE</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("No live orders or external market feeds are connected.")

    st.divider()
    st.markdown('<div class="smallcaps">Workspace profile</div>', unsafe_allow_html=True)
    st.selectbox("Benchmark", ["S&P 500", "MSCI World", "Nasdaq 100"], label_visibility="collapsed")
    st.selectbox("Base currency", ["USD", "EUR", "GBP"], label_visibility="collapsed")

    st.divider()
    st.caption("FinSight Global · Terminal UI v0.2")


# -----------------------------------------------------------------------------
# Global top bar
# -----------------------------------------------------------------------------

st.markdown(
    """
    <div class="topbar">
      <div class="topbar-grid">
        <div class="top-item">
          <div class="top-value"><span class="status-dot"></span>&nbsp; MARKET SESSION OPEN</div>
          <div class="top-note">Demonstration session state</div>
        </div>
        <div class="top-item">
          <div class="top-value">S&P 500&nbsp;&nbsp;6,481.20</div>
          <div class="top-note"><span class="up">+0.82%</span></div>
        </div>
        <div class="top-item">
          <div class="top-value">NASDAQ 100&nbsp;&nbsp;23,914.60</div>
          <div class="top-note"><span class="up">+1.34%</span></div>
        </div>
        <div class="top-item">
          <div class="top-value">BTC / USD&nbsp;&nbsp;113,420</div>
          <div class="top-note"><span class="down">-0.74%</span></div>
        </div>
        <div>
          <span class="pill">DATA: DEMO</span>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Overview
# -----------------------------------------------------------------------------

if page == "Overview":
    st.markdown(
        '<div class="hero"><div class="smallcaps">COMMAND CENTER / OVERVIEW</div>'
        '<h1>Global market intelligence</h1>'
        '<div class="muted">Portfolio state, market regime and AI-generated context in one workspace.</div></div>',
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Portfolio", "$104,284", "+4.28%")
    k2.metric("Today", "+$1,482", "+1.44%")
    k3.metric("Volatility", "14.2%", "Normal")
    k4.metric("Drawdown", "-6.8%", "Current cycle")
    k5.metric("Risk", "32 / 100", "Low")

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    left, mid, right = st.columns([1.7, 1, .9])

    with left:
        st.markdown(
            '<div class="panel"><div class="panel-header">'
            '<div><div class="panel-title">Portfolio performance</div>'
            '<div class="panel-subtitle">180-day indexed demonstration series</div></div>'
            '<span class="pill green">+4.28% YTD</span></div>',
            unsafe_allow_html=True,
        )
        st.line_chart(performance, height=360, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with mid:
        st.markdown(
            '<div class="ai-box"><div class="ai-title">FinSight AI Brief</div>'
            '<div class="ai-headline">Risk is controlled, but concentration is the variable to watch.</div>'
            '<div class="ai-body">The current demonstration portfolio is carrying a relatively balanced overall profile while equity and technology exposure remain the largest contributors to modeled risk.</div>'
            '<div style="margin-top:.65rem"><span class="mini-tag">Concentration</span>'
            '<span class="mini-tag">Momentum</span><span class="mini-tag">Rates</span></div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Signal matrix</div><div class="panel-subtitle">Model state</div></div>', unsafe_allow_html=True)
        matrix = [
            ("Momentum", "72", "up"),
            ("Volatility", "38", "flat"),
            ("Breadth", "64", "up"),
            ("Concentration", "58", "down"),
        ]
        m1, m2 = st.columns(2)
        for idx, (name, value, tone) in enumerate(matrix):
            target = m1 if idx % 2 == 0 else m2
            with target:
                st.markdown(
                    f'<div class="matrix-cell"><div class="matrix-name">{name}</div>'
                    f'<div class="matrix-value {tone}">{value}</div></div><div style="height:.35rem"></div>',
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="panel-header"><div class="panel-title">Watchlist</div>'
            '<div class="panel-subtitle">Core markets</div></div>',
            unsafe_allow_html=True,
        )
        rows = [
            ("SPX", "6,481.2", "+0.82%", "up"),
            ("NDX", "23,914.6", "+1.34%", "up"),
            ("BTC", "113,420", "-0.74%", "down"),
            ("GOLD", "3,812.4", "+0.41%", "up"),
            ("BRENT", "68.7", "-1.18%", "down"),
            ("EURUSD", "1.174", "+0.22%", "up"),
        ]
        st.markdown('<div class="watch-row head"><div>Asset</div><div>Price</div><div class="num">1D</div><div>State</div></div>', unsafe_allow_html=True)
        for symbol, price, change, tone in rows:
            state = "BULL" if tone == "up" else "BEAR"
            st.markdown(
                f'<div class="watch-row"><div><strong>{symbol}</strong></div>'
                f'<div>{price}</div><div class="num {tone}">{change}</div>'
                f'<div class="{tone}">{state}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.25, 1])

    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="panel-header"><div><div class="panel-title">Intelligence feed</div>'
            '<div class="panel-subtitle">Cross-asset context</div></div>'
            '<span class="pill">DEMO</span></div>',
            unsafe_allow_html=True,
        )
        for category, title, timestamp in news:
            st.markdown(
                f'<div class="feed"><div class="feed-title"><span class="mini-tag">{category}</span>{title}</div>'
                f'<div class="feed-meta">{timestamp}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="panel-header"><div><div class="panel-title">Allocation</div>'
            '<div class="panel-subtitle">Strategic mix</div></div></div>',
            unsafe_allow_html=True,
        )
        allocation = pd.Series(
            {"Equities": 44, "Crypto": 14.5, "Gold": 8.5, "Bonds": 7.5, "Cash": 25}
        )
        st.bar_chart(allocation, height=220)
        st.markdown(
            '<div class="muted2" style="font-size:.65rem">Target architecture will become configurable once the portfolio engine is connected.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Markets
# -----------------------------------------------------------------------------

elif page == "Markets":
    st.markdown(
        '<div class="hero"><div class="smallcaps">MARKET MONITOR</div>'
        '<h1>Markets</h1><div class="muted">A dense market surface for prices, momentum, volatility and regime context.</div></div>',
        unsafe_allow_html=True,
    )

    a, b, c, d = st.columns(4)
    a.metric("Market Breadth", "61% Advancing", "+7.2 pts")
    b.metric("Volatility Index", "18.4", "Normal")
    c.metric("Liquidity", "Healthy", "Stable")
    d.metric("Cross-Asset Regime", "Risk-On", "Moderate")

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Overview", "Cross-Asset", "Watchlist"])

    with tab1:
        l, r = st.columns([1.55, 1])
        with l:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-header"><div class="panel-title">Index performance</div><div class="panel-subtitle">Demo session</div></div>', unsafe_allow_html=True)
            index_data = pd.DataFrame(
                {
                    "S&P 500": 100 * np.cumprod(1 + rng.normal(.0004, .009, len(dates))),
                    "Nasdaq 100": 100 * np.cumprod(1 + rng.normal(.0007, .011, len(dates))),
                    "Gold": 100 * np.cumprod(1 + rng.normal(.0002, .007, len(dates))),
                },
                index=dates,
            )
            st.line_chart(index_data, height=360, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with r:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-header"><div class="panel-title">Market map</div><div class="panel-subtitle">Signal distribution</div></div>', unsafe_allow_html=True)
            market_map = pd.DataFrame(
                {
                    "Asset": ["Equities", "Technology", "Crypto", "Gold", "Energy", "FX"],
                    "Signal": [78, 84, 46, 69, 31, 58],
                }
            )
            st.dataframe(
                market_map,
                hide_index=True,
                use_container_width=True,
                column_config={"Signal": st.column_config.ProgressColumn("Signal", min_value=0, max_value=100, format="%d")},
            )
            st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.dataframe(
            assets.style.format({"Price": "{:,.4f}", "1D": "{:+.2f}%", "Vol": "{:.1f}%"}),
            hide_index=True,
            use_container_width=True,
        )

    with tab3:
        query = st.text_input("Search watchlist", placeholder="Symbol or asset name")
        shown = assets if not query else assets[assets.apply(lambda row: query.lower() in row.astype(str).str.lower().str.cat(sep=" "), axis=1)]
        st.dataframe(
            shown.style.format({"Price": "{:,.4f}", "1D": "{:+.2f}%", "Vol": "{:.1f}%"}),
            hide_index=True,
            use_container_width=True,
        )


# -----------------------------------------------------------------------------
# Portfolio
# -----------------------------------------------------------------------------

elif page == "Portfolio":
    st.markdown(
        '<div class="hero"><div class="smallcaps">PORTFOLIO CONTROL</div>'
        '<h1>Portfolio</h1><div class="muted">Positions, attribution, allocation and portfolio-level risk.</div></div>',
        unsafe_allow_html=True,
    )

    a, b, c, d = st.columns(4)
    a.metric("Net Liquidation", "$104,284", "+4.28%")
    b.metric("Unrealized P/L", "+$8,742", "+9.4%")
    c.metric("Sharpe", "1.42", "Demo")
    d.metric("Max Drawdown", "-6.8%", "Demo")

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    l, r = st.columns([1.55, 1])

    with l:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Equity curve</div><div class="panel-subtitle">Portfolio vs benchmark</div></div>', unsafe_allow_html=True)
        st.line_chart(performance, height=360, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Attribution</div><div class="panel-subtitle">Contribution to return</div></div>', unsafe_allow_html=True)
        attrib = pd.Series({"Technology": 3.2, "U.S. Equities": 2.5, "Bitcoin": 0.7, "Gold": 0.5, "Bonds": 0.3, "Cash": 0.0})
        st.bar_chart(attrib, height=315)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header"><div class="panel-title">Holdings</div><div class="panel-subtitle">Position-level demonstration data</div></div>', unsafe_allow_html=True)
    st.dataframe(
        holdings.style.format({"Weight": "{:.1f}%", "P/L": "{:+.1f}%"}),
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Intelligence
# -----------------------------------------------------------------------------

elif page == "Intelligence":
    st.markdown(
        '<div class="hero"><div class="smallcaps">AI RESEARCH DESK</div>'
        '<h1>Intelligence</h1><div class="muted">The future reasoning layer sits on top of market data, portfolio state, analytics and research.</div></div>',
        unsafe_allow_html=True,
    )

    q = st.text_input("Ask FinSight", placeholder="Example: explain the main drivers of current portfolio risk")
    if q:
        st.markdown(
            f'<div class="ai-box"><div class="ai-title">DEMO RESPONSE</div>'
            f'<div class="ai-headline">{html.escape(q)}</div>'
            f'<div class="ai-body">The AI reasoning engine is not connected yet. This surface is intentionally ready for model-backed analysis, source citations, scenario reasoning and portfolio-aware answers.</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    cards = [
        ("Market Intelligence", "Regimes, breadth, momentum, macro drivers and cross-asset relationships.", "MARKET"),
        ("Research Intelligence", "Asset, company, sector and event-level research with source-aware evidence.", "RESEARCH"),
        ("Portfolio Intelligence", "Allocation, performance, attribution, risk contributions and scenario analysis.", "PORTFOLIO"),
    ]
    for target, (title, body, tag) in zip((a, b, c), cards):
        with target:
            st.markdown(
                f'<div class="panel"><span class="mini-tag">{tag}</span>'
                f'<div style="margin-top:.45rem" class="panel-title">{title}</div>'
                f'<div class="feed-body">{body}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    left, right = st.columns([1.25, 1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Analyst workspace</div><div class="panel-subtitle">Prompt → evidence → synthesis</div></div>', unsafe_allow_html=True)
        st.text_area("Research brief", placeholder="Write a question or research task for the future AI engine.", height=150, label_visibility="collapsed")
        st.button("Run analysis", type="primary")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Model context</div><div class="panel-subtitle">Future inputs</div></div>', unsafe_allow_html=True)
        for item, state in [
            ("Market data", "NOT CONNECTED"),
            ("News / research", "NOT CONNECTED"),
            ("Portfolio state", "DEMO"),
            ("Risk engine", "DEMO"),
            ("AI reasoning", "NOT CONNECTED"),
        ]:
            tone = "up" if state == "DEMO" else "flat"
            st.markdown(
                f'<div class="feed"><div class="feed-title">{item}</div>'
                f'<div class="feed-meta {tone}">{state}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Risk
# -----------------------------------------------------------------------------

elif page == "Risk":
    st.markdown(
        '<div class="hero"><div class="smallcaps">RISK CONTROL</div>'
        '<h1>Risk</h1><div class="muted">Portfolio risk surface for exposure, concentration, drawdown and stress.</div></div>',
        unsafe_allow_html=True,
    )

    a, b, c, d = st.columns(4)
    a.metric("Overall Risk", "32 / 100", "Low")
    b.metric("VaR 95%", "$3,180", "1-day demo")
    c.metric("CVaR 95%", "$4,760", "1-day demo")
    d.metric("Stress Loss", "-$8,420", "Market -10%")

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    l, r = st.columns([1.15, .85])

    with l:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Risk domains</div><div class="panel-subtitle">0 = low · 100 = high</div></div>', unsafe_allow_html=True)
        risk = pd.DataFrame(
            {
                "Domain": ["Market", "Concentration", "Liquidity", "Volatility", "Counterparty"],
                "Score": [31, 44, 16, 28, 8],
                "State": ["LOW", "MEDIUM", "LOW", "LOW", "LOW"],
            }
        )
        st.dataframe(
            risk,
            hide_index=True,
            use_container_width=True,
            column_config={"Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d")},
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with r:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Scenario stress</div><div class="panel-subtitle">Modeled portfolio impact</div></div>', unsafe_allow_html=True)
        stress = pd.Series({"Equities -10%": -6.8, "Crypto -25%": -4.1, "Rates +100bp": -4.2, "Oil +20%": 0.7})
        st.bar_chart(stress, height=270)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header"><div class="panel-title">Risk concentration</div><div class="panel-subtitle">Largest modeled exposures</div></div>', unsafe_allow_html=True)
    concentration = pd.DataFrame(
        {
            "Factor": ["Technology", "Equity beta", "Crypto volatility", "USD exposure", "Duration"],
            "Contribution": [26, 22, 19, 12, 8],
        }
    )
    st.dataframe(
        concentration,
        hide_index=True,
        use_container_width=True,
        column_config={"Contribution": st.column_config.ProgressColumn("Contribution", min_value=0, max_value=30, format="%d")},
    )
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Strategies
# -----------------------------------------------------------------------------

elif page == "Strategies":
    st.markdown(
        '<div class="hero"><div class="smallcaps">STRATEGY LAB</div>'
        '<h1>Strategies</h1><div class="muted">Define systematic strategies before routing them into simulation, backtesting or paper execution.</div></div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.2, .8])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Strategy builder</div><div class="panel-subtitle">Configuration workspace</div></div>', unsafe_allow_html=True)
        x1, x2 = st.columns(2)
        with x1:
            signal = st.selectbox("Signal family", ["Momentum", "Mean Reversion", "Macro", "Multi-Factor"])
            rebalance = st.selectbox("Rebalance", ["Daily", "Weekly", "Monthly"])
        with x2:
            risk_model = st.selectbox("Risk model", ["Volatility Target", "Risk Parity", "Fixed Risk", "Adaptive"])
            execution = st.selectbox("Execution", ["Paper", "Backtest", "Simulation"])
        st.slider("Target annualized volatility", 5, 25, 12, 1)
        st.slider("Maximum position weight", 5, 40, 20, 1)
        st.button("Build strategy specification", type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Strategy state</div><div class="panel-subtitle">Selected configuration</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feed"><div class="feed-title">Signal</div><div class="feed-meta">{signal}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feed"><div class="feed-title">Risk model</div><div class="feed-meta">{risk_model}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feed"><div class="feed-title">Rebalance</div><div class="feed-meta">{rebalance}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feed"><div class="feed-title">Execution</div><div class="feed-meta">{execution}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    strategy_table = pd.DataFrame(
        {
            "Strategy": ["Global Momentum", "Risk Parity", "Trend + Macro", "Adaptive Allocation"],
            "State": ["READY", "DESIGN", "DESIGN", "RESEARCH"],
            "Target Vol": ["12%", "10%", "14%", "DYNAMIC"],
            "Next": ["Historical data", "Risk model", "Macro factors", "Signal research"],
        }
    )
    st.dataframe(strategy_table, hide_index=True, use_container_width=True)


# -----------------------------------------------------------------------------
# Backtesting
# -----------------------------------------------------------------------------

elif page == "Backtesting":
    st.markdown(
        '<div class="hero"><div class="smallcaps">QUANT RESEARCH</div>'
        '<h1>Backtesting</h1><div class="muted">Research strategies against historical data with transaction costs, slippage and risk metrics.</div></div>',
        unsafe_allow_html=True,
    )

    a, b, c, d = st.columns(4)
    a.metric("CAGR", "14.8%", "Demo")
    b.metric("Sharpe", "1.31", "Demo")
    c.metric("Max Drawdown", "-11.4%", "Demo")
    d.metric("Win Rate", "58.2%", "Demo")

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    left, right = st.columns([1.5, .7])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Backtest equity curve</div><div class="panel-subtitle">Demonstration result</div></div>', unsafe_allow_html=True)
        backtest_curve = pd.DataFrame(
            {
                "Strategy": 100 * np.cumprod(1 + rng.normal(.0008, .012, len(dates))),
                "Benchmark": 100 * np.cumprod(1 + rng.normal(.0005, .010, len(dates))),
            },
            index=dates,
        )
        st.line_chart(backtest_curve, height=360, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Run configuration</div><div class="panel-subtitle">Future engine inputs</div></div>', unsafe_allow_html=True)
        st.selectbox("Strategy", ["Global Momentum", "Risk Parity", "Trend + Macro"])
        st.selectbox("Universe", ["Global Equities", "Multi-Asset", "Crypto + Equities"])
        st.select_slider("Period", options=["1Y", "3Y", "5Y", "10Y"], value="5Y")
        st.number_input("Transaction cost (bps)", min_value=0, max_value=100, value=5)
        st.button("Run backtest", type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    stats = pd.DataFrame(
        {
            "Metric": ["CAGR", "Volatility", "Sharpe", "Sortino", "Max Drawdown", "VaR 95%"],
            "Strategy": ["14.8%", "12.3%", "1.31", "1.86", "-11.4%", "-2.7%"],
            "Benchmark": ["11.2%", "15.1%", "0.94", "1.33", "-18.9%", "-3.5%"],
        }
    )
    st.dataframe(stats, hide_index=True, use_container_width=True)


# -----------------------------------------------------------------------------
# Execution
# -----------------------------------------------------------------------------

elif page == "Execution":
    st.markdown(
        '<div class="hero"><div class="smallcaps">ORDER MANAGEMENT</div>'
        '<h1>Execution</h1><div class="muted">Paper execution control room. Live routing remains disabled.</div></div>',
        unsafe_allow_html=True,
    )

    st.warning("PAPER / SIMULATION ONLY — no live broker orders are connected.")

    l, r = st.columns([1, 1.25])
    with l:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Order staging</div><div class="panel-subtitle">No live submission</div></div>', unsafe_allow_html=True)
        asset = st.text_input("Asset", "SPY")
        qty = st.number_input("Quantity", min_value=0.0, value=10.0, step=1.0)
        side = st.selectbox("Side", ["BUY", "SELL"])
        order_type = st.selectbox("Order type", ["MARKET", "LIMIT", "STOP"])
        limit_price = st.number_input("Limit / trigger price", min_value=0.0, value=0.0, step=0.01)
        st.button("Stage paper order", type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    with r:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Order blotter</div><div class="panel-subtitle">Demonstration history</div></div>', unsafe_allow_html=True)
        orders = pd.DataFrame(
            {
                "Time": ["09:42", "10:18", "11:07", "11:32"],
                "Asset": ["SPY", "BTC", "GLD", "QQQ"],
                "Side": ["BUY", "BUY", "SELL", "BUY"],
                "Qty": [12, 0.025, 8, 6],
                "Status": ["SIMULATED", "SIMULATED", "SIMULATED", "STAGED"],
            }
        )
        st.dataframe(orders, hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header"><div class="panel-title">Execution pipeline</div><div class="panel-subtitle">Target architecture</div></div>', unsafe_allow_html=True)
    pipeline = ["Signal", "Risk check", "Position check", "Order validation", "Broker adapter", "Fill", "Portfolio update", "Audit"]
    cols = st.columns(len(pipeline))
    for col, stage in zip(cols, pipeline):
        with col:
            st.markdown(
                f'<div class="matrix-cell"><div class="matrix-name">{stage.upper()}</div>'
                f'<div class="matrix-value flat">READY</div></div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Alerts
# -----------------------------------------------------------------------------

else:
    st.markdown(
        '<div class="hero"><div class="smallcaps">MONITORING</div>'
        '<h1>Alerts</h1><div class="muted">Market, portfolio and AI event monitoring.</div></div>',
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)
    a.metric("Open Alerts", "3", "+1 today")
    b.metric("Acknowledged", "5", "This week")
    c.metric("Rules Active", "7", "Demo")

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    left, right = st.columns([1.3, .7])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Alert feed</div><div class="panel-subtitle">Latest events</div></div>', unsafe_allow_html=True)
        alerts = pd.DataFrame(
            {
                "Severity": ["MEDIUM", "LOW", "LOW", "INFO"],
                "Alert": [
                    "Technology concentration above target",
                    "Gold momentum improving",
                    "Volatility normalizing",
                    "Portfolio rebalance window approaching",
                ],
                "State": ["OPEN", "OPEN", "ACKNOWLEDGED", "OPEN"],
            }
        )
        st.dataframe(alerts, hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Alert rules</div><div class="panel-subtitle">Monitoring switches</div></div>', unsafe_allow_html=True)
        st.checkbox("Drawdown threshold", value=True)
        st.checkbox("Volatility regime change", value=True)
        st.checkbox("Concentration threshold", value=True)
        st.checkbox("AI anomaly detection", value=False)
        st.checkbox("Macro event monitor", value=True)
        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------

st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="muted2" style="font-size:.63rem;text-align:right">'
    'FINSIGHT GLOBAL · TERMINAL UI v0.2 · DEMONSTRATION DATA ONLY'
    '</div>',
    unsafe_allow_html=True,
)
