import html
import numpy as np
import pandas as pd
import streamlit as st

from replay_lab import render_replay_lab

st.set_page_config(
    page_title="FinSight Global",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root{color-scheme:dark;--bg:#05070b;--panel:#0a0e14;--line:#1a2330;--line2:#263443;--text:#edf2f7;--muted:#7f8b9a;--muted2:#596575;--cyan:#63d7ff;--green:#43d17a;--red:#ff6176;--amber:#e9ad4b;--violet:#9f8bff}
html,body,[class*="css"]{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.stApp{background:radial-gradient(circle at 85% 0%,rgba(50,110,160,.10),transparent 30%),radial-gradient(circle at 10% 100%,rgba(80,60,170,.07),transparent 28%),var(--bg)}
.block-container{max-width:1780px;padding:1.1rem 1.5rem 3rem}
[data-testid="stSidebar"]{background:#070a0f;border-right:1px solid var(--line)}
[data-testid="stSidebar"]>div:first-child{padding:.9rem .75rem 1.2rem}
[data-testid="stSidebar"] *{color:var(--text)}
[data-testid="stSidebar"] hr{border-color:var(--line);margin:.8rem 0}
[data-testid="stSidebar"] .stRadio>label{color:var(--muted);font-size:.66rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase}
[data-testid="stSidebar"] [role="radiogroup"]{gap:.15rem}
[data-testid="stSidebar"] [role="radio"]{border-radius:8px;padding:.42rem .55rem}
[data-testid="stSidebar"] [role="radio"]:hover{background:#0f151d}
[data-testid="stSidebar"] [role="radio"][aria-checked="true"]{background:#101a24;border:1px solid #1d3948}
[data-testid="stSidebar"] [role="radio"] p{font-size:.86rem}
[data-testid="stSidebar"] [data-testid="stMetric"]{padding:.55rem .6rem;margin-bottom:.35rem;background:#0a0f15}
h1,h2,h3,h4{letter-spacing:-.03em}h1{font-size:2.15rem!important;margin:0!important}h2{font-size:1.25rem!important}h3{font-size:1rem!important}
p{line-height:1.45}
[data-testid="stMetric"]{background:linear-gradient(145deg,#0c1118,#080c11);border:1px solid var(--line);border-radius:12px;padding:.75rem .85rem}
[data-testid="stMetricLabel"]{color:var(--muted)!important;font-size:.69rem!important;text-transform:uppercase;letter-spacing:.08em}
[data-testid="stMetricValue"]{color:var(--text)!important;font-size:1.5rem!important}
[data-testid="stMetricDelta"]{font-size:.72rem!important}
.stButton>button{border:1px solid var(--line2);background:#0d131b;color:var(--text);border-radius:8px}
.stButton>button:hover{border-color:#2f6074;color:#fff}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:10px;overflow:hidden}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stSelectbox"] div[data-baseweb="select"]>div{background:#090d13;border-color:var(--line2)}
[data-testid="stTabs"] button{color:var(--muted)}[data-testid="stTabs"] button[aria-selected="true"]{color:var(--text)}
hr{border-color:var(--line)}
.smallcaps{color:var(--muted);font-size:.64rem;font-weight:800;letter-spacing:.15em;text-transform:uppercase}
.muted{color:var(--muted)}.muted2{color:var(--muted2)}
.app-mark{font-size:1.2rem;font-weight:900;letter-spacing:-.05em}
.rail-card{border:1px solid var(--line);background:#0a0f15;border-radius:9px;padding:.65rem .7rem;margin:.35rem 0}
.rail-row{display:flex;justify-content:space-between;gap:.5rem;align-items:center;padding:.22rem 0;font-size:.69rem}
.rail-label{color:var(--muted)}.rail-value{font-weight:700;font-variant-numeric:tabular-nums}
.status-dot{width:7px;height:7px;border-radius:50%;display:inline-block;background:var(--green);box-shadow:0 0 10px rgba(67,209,122,.55)}
.pill{display:inline-flex;align-items:center;gap:.35rem;border:1px solid var(--line2);border-radius:999px;padding:.23rem .5rem;color:#b7c3cf;background:#0c1219;font-size:.62rem;font-weight:750;letter-spacing:.05em;text-transform:uppercase}
.pill.green{color:#8ef0b0;border-color:#1f5134;background:#0c1811}.pill.amber{color:#f3c86e;border-color:#5d451f;background:#191309}.pill.red{color:#ff96a4;border-color:#5b2630;background:#190b0e}
.hero{padding:.2rem 0 .85rem}.hero h1{font-size:2.3rem!important}.hero-sub{margin-top:.15rem;color:var(--muted)}
.panel{background:linear-gradient(155deg,rgba(14,19,27,.98),rgba(8,12,17,.98));border:1px solid var(--line);border-radius:12px;padding:.9rem}
.panel-header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.7rem}
.panel-title{font-size:.9rem;font-weight:800;color:var(--text)}.panel-subtitle{color:var(--muted);font-size:.66rem}
.feed{padding:.65rem 0;border-top:1px solid var(--line)}.feed:first-child{border-top:0;padding-top:0}
.feed-title{color:var(--text);font-size:.79rem;font-weight:750}.feed-body{color:var(--muted);font-size:.71rem;line-height:1.45;margin-top:.15rem}.feed-meta{color:var(--muted2);font-size:.62rem;margin-top:.28rem}
.ai-box{border:1px solid #263247;background:radial-gradient(circle at 88% 16%,rgba(117,102,255,.18),transparent 28%),linear-gradient(150deg,#111527,#0a0f18);border-radius:12px;padding:.9rem}
.ai-title{color:#c9c3ff;font-size:.66rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase}
.ai-headline{margin-top:.2rem;color:#f1efff;font-size:1rem;font-weight:800}.ai-body{margin-top:.35rem;color:#9ca3b8;font-size:.72rem;line-height:1.5}
.mini-tag{display:inline-block;padding:.16rem .38rem;margin-right:.22rem;border:1px solid #293343;border-radius:5px;color:#9aa8b8;background:#0c121a;font-size:.6rem}
.matrix-cell{padding:.55rem;border:1px solid var(--line);background:#0a0f15;border-radius:8px;min-height:70px}
.matrix-name{font-size:.66rem;color:var(--muted)}.matrix-value{font-size:.98rem;font-weight:800;margin-top:.2rem}
.up{color:var(--green)}.down{color:var(--red)}.flat{color:var(--muted)}
.section-gap{height:.45rem}
.watch-row{display:grid;grid-template-columns:1.1fr .9fr .7fr .55fr;gap:.3rem;align-items:center;padding:.5rem .02rem;border-top:1px solid var(--line);font-size:.7rem}
.watch-row.head{color:var(--muted2);font-size:.59rem;letter-spacing:.08em;text-transform:uppercase;border-top:0}.num{text-align:right;font-variant-numeric:tabular-nums}
</style>
""", unsafe_allow_html=True)

rng = np.random.default_rng(17)
dates = pd.date_range(end=pd.Timestamp.now().normalize(), periods=180, freq="D")
portfolio_curve = 100_000 * np.cumprod(1 + rng.normal(.00062, .0115, len(dates)))
benchmark_curve = 100_000 * np.cumprod(1 + rng.normal(.00051, .0104, len(dates)))
performance = pd.DataFrame({"FinSight Portfolio": portfolio_curve, "Benchmark": benchmark_curve}, index=dates)

assets = pd.DataFrame({
    "Symbol":["SPX","NDX","BTC","GOLD","BRENT","EURUSD"],
    "Instrument":["S&P 500","Nasdaq 100","Bitcoin","Gold","Brent Crude","Euro / U.S. Dollar"],
    "Price":[6481.2,23914.6,113420.0,3812.4,68.7,1.174],
    "1D":[.82,1.34,-.74,.41,-1.18,.22],
    "Signal":["BULLISH","BULLISH","NEUTRAL","BULLISH","BEARISH","NEUTRAL"],
    "Vol":[14.2,17.8,48.1,16.7,29.3,7.9],
})
holdings = pd.DataFrame({
    "Symbol":["VOO","QQQ","BTC","GLD","TLT","CASH"],
    "Position":["U.S. Equities","Technology","Bitcoin","Gold","Treasuries","Cash"],
    "Weight":[27.5,17.0,14.5,8.5,7.5,25.0],
    "P/L":[8.4,11.2,3.1,5.7,1.8,0.0],
    "Risk":["MED","HIGH","HIGH","LOW","LOW","LOW"],
})
news = [
    ("Macro","Rates remain the primary cross-asset sensitivity.","12 min ago"),
    ("Equities","Technology leadership remains positive but concentrated.","24 min ago"),
    ("Crypto","Bitcoin volatility remains materially above major equity indices.","39 min ago"),
    ("Commodities","Energy weakness is pressuring the near-term inflation impulse.","51 min ago"),
]

NAV = ["Overview","Markets","Portfolio","Intelligence","Risk","Strategies","Backtesting","Replay Lab","Execution","Alerts"]

@st.fragment(run_every=1.5, key="market_stream")
def render_markets_workspace():
        st.markdown('<div class="hero"><div class="smallcaps">LIVE MARKET LAB</div><h1>Markets</h1><div class="hero-sub">Streaming OHLCV charts, regime detection and paper-only chart actions.</div></div>', unsafe_allow_html=True)
    
        import plotly.graph_objects as go
        from market_engine import seed_ohlcv, advance_ohlcv, analyze_market, analyze_chart_type, fetch_live_ohlcv
    
        symbols = ["SPX", "NDX", "BTC", "GOLD", "BRENT", "EURUSD"]
        profiles = {
            "SPX": "S&P 500",
            "NDX": "Nasdaq 100",
            "BTC": "Bitcoin",
            "GOLD": "Gold",
            "BRENT": "Brent Crude",
            "EURUSD": "Euro / U.S. Dollar",
        }
    
        if "market_streams" not in st.session_state:
            st.session_state.market_streams = {
                symbol: seed_ohlcv(symbol, bars=240, seed=17)
                for symbol in symbols
            }
        if "paper_actions" not in st.session_state:
            st.session_state.paper_actions = []
        if "last_paper_action" not in st.session_state:
            st.session_state.last_paper_action = {}
        if "live_data_cache" not in st.session_state:
            st.session_state.live_data_cache = {}
    
        a, b, c, d = st.columns(4)
        selected_symbol = a.selectbox(
            "Instrument",
            symbols,
            format_func=lambda s: f"{s} · {profiles[s]}",
        )
        chart_type = b.selectbox(
            "Chart type",
            ["Candlestick", "Line + trend", "Area", "MACD momentum", "RSI", "Volume", "Return distribution"],
        )
        source = c.selectbox("Data source", ["Simulation", "Live / Yahoo Finance"])
        auto_refresh = d.toggle("Streaming", value=True)
    
        # Live provider: refresh the selected instrument; cache failures back to simulation.
        data_is_live = False
        if source == "Live / Yahoo Finance":
            live = fetch_live_ohlcv(selected_symbol)
            if live is not None and len(live) >= 60:
                frame = live
                st.session_state.market_streams[selected_symbol] = frame
                st.session_state.live_data_cache[selected_symbol] = frame
                data_is_live = True
            else:
                frame = st.session_state.live_data_cache.get(selected_symbol, st.session_state.market_streams[selected_symbol])
                st.info("Live provider returned no usable bars for this instrument; showing the latest available stream.")
        else:
            if auto_refresh or "market_tick" not in st.session_state:
                st.session_state.market_streams[selected_symbol] = advance_ohlcv(
                    st.session_state.market_streams[selected_symbol]
                )
            frame = st.session_state.market_streams[selected_symbol]
    
        st.session_state.market_tick = st.session_state.get("market_tick", 0) + 1
        analysis = analyze_chart_type(frame, chart_type)
        data = analysis["data"]
    
        action = analysis["action"]
        action_class = "up" if action == "PAPER BUY" else "down" if action == "PAPER SELL" else "flat"
        regime_class = "up" if analysis["regime"] == "BULLISH" else "down" if analysis["regime"] == "BEARISH" else "flat"
        source_label = "LIVE" if data_is_live else "SIMULATION"
    
        if "auto_action" not in st.session_state:
            st.session_state.auto_action = False
        st.session_state.auto_action = st.toggle(
            "Paper auto-action",
            value=st.session_state.auto_action,
            help="Records simulated BUY/SELL events when the chart intelligence engine crosses an action threshold. No live order is sent.",
        )
    
        if st.session_state.auto_action and action != "HOLD":
            previous = st.session_state.last_paper_action.get(selected_symbol)
            if previous != action:
                st.session_state.paper_actions.insert(
                    0,
                    {
                        "Timestamp": pd.Timestamp.now().strftime("%H:%M:%S"),
                        "Symbol": selected_symbol,
                        "Action": action,
                        "Regime": analysis["regime"],
                        "Score": analysis["score"],
                        "Confidence": f"{analysis['confidence']}%",
                        "Pattern": analysis["pattern"],
                        "Source": source_label,
                    },
                )
                st.session_state.last_paper_action[selected_symbol] = action
                st.session_state.paper_actions = st.session_state.paper_actions[:20]
    
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Last price", f"{analysis['price']:,.4f}")
        m2.metric("Bar return", f"{data['Return1'].iloc[-1]:+.2f}%")
        m3.metric("Regime", analysis["regime"], f"Score {analysis['score']:+d}")
        m4.metric("RSI 14", f"{analysis['rsi']:.1f}", "Momentum")
        m5.metric("Decision", action, f"{analysis['confidence']}% confidence")
    
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        left, right = st.columns([1.65, .8])
    
        with left:
            regime_pill = "green" if analysis["regime"] == "BULLISH" else "red" if analysis["regime"] == "BEARISH" else ""
            st.markdown(
                f'<div class="panel"><div class="panel-header">'
                f'<div><div class="panel-title">{selected_symbol} · {profiles[selected_symbol]}</div>'
                f'<div class="panel-subtitle">5-minute bars · {source_label} · tick {st.session_state.market_tick}</div></div>'
                f'<span class="pill {regime_pill}">{analysis["regime"]}</span></div>',
                unsafe_allow_html=True,
            )
    
            visible = data.tail(100)
            fig = go.Figure()
    
            if chart_type == "Candlestick":
                fig.add_trace(go.Candlestick(
                    x=visible.index,
                    open=visible["Open"],
                    high=visible["High"],
                    low=visible["Low"],
                    close=visible["Close"],
                    name="OHLC",
                    increasing_line_color="#43d17a",
                    decreasing_line_color="#ff6176",
                ))
                fig.add_trace(go.Scatter(
                    x=visible.index, y=visible["SMA20"], mode="lines",
                    name="SMA20", line=dict(color="#63d7ff", width=1.4)
                ))
                fig.add_trace(go.Scatter(
                    x=visible.index, y=visible["SMA50"], mode="lines",
                    name="SMA50", line=dict(color="#9f8bff", width=1.2)
                ))
            elif chart_type == "Line + trend":
                fig.add_trace(go.Scatter(
                    x=visible.index, y=visible["Close"], mode="lines",
                    name="Close", line=dict(color="#63d7ff", width=2)
                ))
                fig.add_trace(go.Scatter(
                    x=visible.index, y=visible["EMA12"], mode="lines",
                    name="EMA12", line=dict(color="#43d17a", width=1.2)
                ))
                fig.add_trace(go.Scatter(
                    x=visible.index, y=visible["EMA26"], mode="lines",
                    name="EMA26", line=dict(color="#e9ad4b", width=1.2)
                ))
            elif chart_type == "Area":
                fig.add_trace(go.Scatter(
                    x=visible.index, y=visible["Close"], mode="lines", fill="tozeroy",
                    name="Price", line=dict(color="#63d7ff", width=1.8)
                ))
            elif chart_type == "MACD momentum":
                fig.add_trace(go.Bar(x=visible.index, y=visible["MACDHist"], name="Histogram"))
                fig.add_trace(go.Scatter(
                    x=visible.index, y=visible["MACD"], mode="lines",
                    name="MACD", line=dict(color="#63d7ff", width=1.6)
                ))
                fig.add_trace(go.Scatter(
                    x=visible.index, y=visible["MACDSignal"], mode="lines",
                    name="Signal", line=dict(color="#e9ad4b", width=1.2)
                ))
            elif chart_type == "RSI":
                fig.add_trace(go.Scatter(
                    x=visible.index, y=visible["RSI14"], mode="lines",
                    name="RSI 14", line=dict(color="#9f8bff", width=1.8)
                ))
                fig.add_hline(y=70, line_dash="dot", line_color="#ff6176")
                fig.add_hline(y=30, line_dash="dot", line_color="#43d17a")
                fig.update_yaxes(range=[0, 100])
            elif chart_type == "Volume":
                fig.add_trace(go.Bar(x=visible.index, y=visible["Volume"], name="Volume"))
                fig.add_trace(go.Scatter(
                    x=visible.index, y=visible["VolumeMA20"], mode="lines",
                    name="Volume MA20", line=dict(color="#63d7ff", width=1.2)
                ))
            else:
                fig.add_trace(go.Histogram(
                    x=data["Return1"].dropna(), nbinsx=35, name="1-bar returns"
                ))
    
            fig.update_layout(
                height=500,
                margin=dict(l=5, r=5, t=10, b=5),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#edf2f7", size=11),
                xaxis=dict(showgrid=False, rangeslider=dict(visible=False)),
                yaxis=dict(showgrid=True, gridcolor="rgba(128,145,160,.10)", zeroline=False),
                legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0),
                hovermode="x unified",
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)
    
        with right:
            st.markdown(
                f'<div class="ai-box"><div class="ai-title">CHART INTELLIGENCE ENGINE</div>'
                f'<div class="ai-headline {regime_class}">{analysis["regime"]} · {action}</div>'
                f'<div class="ai-body">Trend alignment, MACD, RSI, candle structure, range breaks and volatility are combined into a paper-trading state.</div>'
                f'<div style="margin-top:.55rem"><span class="mini-tag">{analysis["pattern"]}</span>'
                f'<span class="mini-tag">RSI {analysis["rsi"]:.1f}</span><span class="mini-tag">ATR {analysis["atr_pct"]:.2f}%</span>'
                f'<span class="mini-tag">{source_label}</span></div></div>',
                unsafe_allow_html=True,
            )
    
            st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-header"><div class="panel-title">Reasoning trace</div><div class="panel-subtitle">Explainable signal inputs</div></div>', unsafe_allow_html=True)
            for reason in analysis["reasons"]:
                st.markdown(f'<div class="feed"><div class="feed-title">{html.escape(reason)}</div></div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
            st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-header"><div class="panel-title">Paper action control</div><div class="panel-subtitle">Simulation only</div></div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="matrix-cell"><div class="matrix-name">ENGINE DECISION</div>'
                f'<div class="matrix-value {action_class}">{action}</div>'
                f'<div class="feed-meta">Confidence {analysis["confidence"]}% · Score {analysis["score"]:+d}</div></div>',
                unsafe_allow_html=True,
            )
            st.caption("This engine records simulated actions only. It cannot submit a live broker order.")
            st.markdown("</div>", unsafe_allow_html=True)
    
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Multi-market regime board</div><div class="panel-subtitle">Simulation board; selected live feed is shown above when enabled.</div></div>', unsafe_allow_html=True)
        rows = []
        for symbol in symbols:
            current = st.session_state.market_streams[symbol]
            result = analyze_market(current)
            rows.append({
                "Symbol": symbol,
                "Price": result["price"],
                "Regime": result["regime"],
                "Score": result["score"],
                "Action": result["action"],
                "Confidence": f"{result['confidence']}%",
                "Pattern": result["pattern"],
            })
        st.dataframe(pd.DataFrame(rows).style.format({"Price": "{:,.4f}", "Score": "{:+d}"}), hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div class="panel-title">Paper action ledger</div><div class="panel-subtitle">Triggered by the chart intelligence engine</div></div>', unsafe_allow_html=True)
        if st.session_state.paper_actions:
            st.dataframe(pd.DataFrame(st.session_state.paper_actions), hide_index=True, use_container_width=True)
        else:
            st.caption("No paper actions recorded. Enable Paper auto-action and wait for a signal transition.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    
    

@st.fragment(key="finsight_app")
def render_finsight_app():
    with st.sidebar:
        st.markdown('<div class="app-mark">◈ FINSIGHT</div>', unsafe_allow_html=True)
        st.markdown('<div class="smallcaps">GLOBAL INTELLIGENCE TERMINAL</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
    
        st.markdown('<div class="rail-card">', unsafe_allow_html=True)
        st.markdown('<div class="smallcaps">Terminal status</div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top:.35rem'><span class='pill green'><span class='status-dot'></span> PAPER MODE</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='rail-row'><span class='rail-label'>Session</span><span class='rail-value'>OPEN</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='rail-row'><span class='rail-label'>Data</span><span class='rail-value'>DEMO</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='rail-row'><span class='rail-label'>Orders</span><span class='rail-value'>DISABLED</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
        st.markdown('<div class="smallcaps" style="margin:.9rem 0 .35rem">Workspace</div>', unsafe_allow_html=True)
        page = st.radio("WORKSPACE", NAV, index=0, label_visibility="collapsed")
    
        st.divider()
        st.markdown('<div class="smallcaps">Live watch</div>', unsafe_allow_html=True)
        for symbol, value, change, tone in [
            ("SPX","6,481.20","+0.82%","up"),
            ("NDX","23,914.60","+1.34%","up"),
            ("BTC","113,420","-0.74%","down"),
            ("GOLD","3,812.40","+0.41%","up"),
        ]:
            st.markdown(
                f"<div class='rail-row'><span class='rail-label'><strong>{symbol}</strong></span>"
                f"<span class='rail-value'>{value} <span class='{tone}'>{change}</span></span></div>",
                unsafe_allow_html=True,
            )
    
        st.divider()
        st.markdown('<div class="smallcaps">Market context</div>', unsafe_allow_html=True)
        st.metric("Breadth", "61%", "+7.2 pts")
        st.metric("Volatility", "18.4", "Normal")
        st.metric("Portfolio risk", "32 / 100", "Low")
    
        st.divider()
        st.markdown('<div class="smallcaps">Workspace profile</div>', unsafe_allow_html=True)
        st.selectbox("Benchmark", ["S&P 500","MSCI World","Nasdaq 100"], label_visibility="collapsed")
        st.selectbox("Base currency", ["USD","EUR","GBP"], label_visibility="collapsed")
        st.caption("FinSight Global · Terminal UI v0.3")
    
    if page == "Overview":
        st.markdown('<div class="hero"><div class="smallcaps">COMMAND CENTER / OVERVIEW</div><h1>Global market intelligence</h1><div class="hero-sub">Portfolio state, market regime and AI-generated context in one workspace.</div></div>', unsafe_allow_html=True)
        a,b,c,d,e = st.columns(5)
        a.metric("Portfolio","$104,284","+4.28%")
        b.metric("Today","+$1,482","+1.44%")
        c.metric("Volatility","14.2%","Normal")
        d.metric("Drawdown","-6.8%","Current cycle")
        e.metric("Risk","32 / 100","Low")
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        left,mid,right = st.columns([1.7,1,.9])
        with left:
            st.markdown('<div class="panel"><div class="panel-header"><div><div class="panel-title">Portfolio performance</div><div class="panel-subtitle">180-day indexed demonstration series</div></div><span class="pill green">+4.28% YTD</span></div>', unsafe_allow_html=True)
            st.line_chart(performance, height=350, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with mid:
            st.markdown('<div class="ai-box"><div class="ai-title">FinSight AI Brief</div><div class="ai-headline">Risk is controlled, but concentration is the variable to watch.</div><div class="ai-body">The current demonstration portfolio is balanced overall while equity and technology exposure remain the largest contributors to modeled risk.</div><div style="margin-top:.6rem"><span class="mini-tag">Concentration</span><span class="mini-tag">Momentum</span><span class="mini-tag">Rates</span></div></div>', unsafe_allow_html=True)
            st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Signal matrix</div><div class="panel-subtitle">Model state</div></div>', unsafe_allow_html=True)
            vals=[("Momentum","72","up"),("Volatility","38","flat"),("Breadth","64","up"),("Concentration","58","down")]
            x,y=st.columns(2)
            for i,(name,val,tone) in enumerate(vals):
                with (x if i%2==0 else y):
                    st.markdown(f'<div class="matrix-cell"><div class="matrix-name">{name}</div><div class="matrix-value {tone}">{val}</div></div><div style="height:.35rem"></div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Watchlist</div><div class="panel-subtitle">Core markets</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="watch-row head"><div>Asset</div><div>Price</div><div class="num">1D</div><div>State</div></div>', unsafe_allow_html=True)
            for symbol,price,change,tone in [("SPX","6,481.2","+0.82%","up"),("NDX","23,914.6","+1.34%","up"),("BTC","113,420","-0.74%","down"),("GOLD","3,812.4","+0.41%","up"),("BRENT","68.7","-1.18%","down"),("EURUSD","1.174","+0.22%","up")]:
                state="BULL" if tone=="up" else "BEAR"
                st.markdown(f'<div class="watch-row"><div><strong>{symbol}</strong></div><div>{price}</div><div class="num {tone}">{change}</div><div class="{tone}">{state}</div></div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        l,r=st.columns([1.25,1])
        with l:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Intelligence feed</div><div class="panel-subtitle">Cross-asset context</div></div>', unsafe_allow_html=True)
            for category,title,timestamp in news:
                st.markdown(f'<div class="feed"><div class="feed-title"><span class="mini-tag">{category}</span>{title}</div><div class="feed-meta">{timestamp}</div></div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with r:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Allocation</div><div class="panel-subtitle">Strategic mix</div></div>', unsafe_allow_html=True)
            st.bar_chart(pd.Series({"Equities":44,"Crypto":14.5,"Gold":8.5,"Bonds":7.5,"Cash":25}), height=220)
            st.markdown("</div>", unsafe_allow_html=True)
    
    elif page == "Markets":
        render_markets_workspace()
    
    elif page == "Portfolio":
        st.markdown('<div class="hero"><div class="smallcaps">PORTFOLIO CONTROL</div><h1>Portfolio</h1><div class="hero-sub">Positions, attribution, allocation and portfolio-level risk.</div></div>', unsafe_allow_html=True)
        a,b,c,d=st.columns(4); a.metric("Net Liquidation","$104,284","+4.28%"); b.metric("Unrealized P/L","+$8,742","+9.4%"); c.metric("Sharpe","1.42","Demo"); d.metric("Max Drawdown","-6.8%","Demo")
        l,r=st.columns([1.55,1])
        with l:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Equity curve</div><div class="panel-subtitle">Portfolio vs benchmark</div></div>',unsafe_allow_html=True); st.line_chart(performance,height=350,use_container_width=True); st.markdown("</div>",unsafe_allow_html=True)
        with r:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Attribution</div><div class="panel-subtitle">Contribution to return</div></div>',unsafe_allow_html=True); st.bar_chart(pd.Series({"Technology":3.2,"U.S. Equities":2.5,"Bitcoin":.7,"Gold":.5,"Bonds":.3,"Cash":0}),height=305); st.markdown("</div>",unsafe_allow_html=True)
        st.markdown('<div class="section-gap"></div>',unsafe_allow_html=True)
        st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Holdings</div><div class="panel-subtitle">Position-level demonstration data</div></div>',unsafe_allow_html=True); st.dataframe(holdings.style.format({"Weight":"{:.1f}%","P/L":"{:+.1f}%"}),hide_index=True,use_container_width=True); st.markdown("</div>",unsafe_allow_html=True)
    
    elif page == "Intelligence":
        st.markdown('<div class="hero"><div class="smallcaps">AI RESEARCH DESK</div><h1>Intelligence</h1><div class="hero-sub">A future reasoning layer over market data, portfolio state, analytics and research.</div></div>',unsafe_allow_html=True)
        q=st.text_input("Ask FinSight",placeholder="Explain the main drivers of current portfolio risk")
        if q: st.markdown(f'<div class="ai-box"><div class="ai-title">DEMO RESPONSE</div><div class="ai-headline">{html.escape(q)}</div><div class="ai-body">The AI reasoning engine is not connected yet. This surface is ready for model-backed analysis, evidence, scenario reasoning and portfolio-aware answers.</div></div>',unsafe_allow_html=True)
        a,b,c=st.columns(3)
        for col,title,body,tag in [(a,"Market Intelligence","Regimes, breadth, momentum, macro drivers and cross-asset relationships.","MARKET"),(b,"Research Intelligence","Asset, company, sector and event-level research with source-aware evidence.","RESEARCH"),(c,"Portfolio Intelligence","Allocation, performance, attribution, risk contributions and scenarios.","PORTFOLIO")]:
            with col: st.markdown(f'<div class="panel"><span class="mini-tag">{tag}</span><div style="margin-top:.4rem" class="panel-title">{title}</div><div class="feed-body">{body}</div></div>',unsafe_allow_html=True)
        l,r=st.columns([1.25,1])
        with l:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Analyst workspace</div><div class="panel-subtitle">Prompt → evidence → synthesis</div></div>',unsafe_allow_html=True); st.text_area("Research brief",placeholder="Write a question or research task.",height=145,label_visibility="collapsed"); st.button("Run analysis",type="primary"); st.markdown("</div>",unsafe_allow_html=True)
        with r:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Model context</div><div class="panel-subtitle">Future inputs</div></div>',unsafe_allow_html=True)
            for item,state in [("Market data","NOT CONNECTED"),("News / research","NOT CONNECTED"),("Portfolio state","DEMO"),("Risk engine","DEMO"),("AI reasoning","NOT CONNECTED")]:
                tone="up" if state=="DEMO" else "flat"; st.markdown(f'<div class="feed"><div class="feed-title">{item}</div><div class="feed-meta {tone}">{state}</div></div>',unsafe_allow_html=True)
            st.markdown("</div>",unsafe_allow_html=True)
    
    elif page == "Risk":
        st.markdown('<div class="hero"><div class="smallcaps">RISK CONTROL</div><h1>Risk</h1><div class="hero-sub">Exposure, concentration, drawdown and scenario stress.</div></div>',unsafe_allow_html=True)
        a,b,c,d=st.columns(4); a.metric("Overall Risk","32 / 100","Low"); b.metric("VaR 95%","$3,180","1-day demo"); c.metric("CVaR 95%","$4,760","1-day demo"); d.metric("Stress Loss","-$8,420","Market -10%")
        l,r=st.columns([1.15,.85])
        with l:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Risk domains</div><div class="panel-subtitle">0 = low · 100 = high</div></div>',unsafe_allow_html=True)
            risk=pd.DataFrame({"Domain":["Market","Concentration","Liquidity","Volatility","Counterparty"],"Score":[31,44,16,28,8],"State":["LOW","MEDIUM","LOW","LOW","LOW"]})
            st.dataframe(risk,hide_index=True,use_container_width=True,column_config={"Score":st.column_config.ProgressColumn("Score",min_value=0,max_value=100,format="%d")}); st.markdown("</div>",unsafe_allow_html=True)
        with r:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Scenario stress</div><div class="panel-subtitle">Modeled portfolio impact</div></div>',unsafe_allow_html=True); st.bar_chart(pd.Series({"Equities -10%":-6.8,"Crypto -25%":-4.1,"Rates +100bp":-4.2,"Oil +20%":.7}),height=260); st.markdown("</div>",unsafe_allow_html=True)
        st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Risk concentration</div><div class="panel-subtitle">Largest modeled exposures</div></div>',unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({"Factor":["Technology","Equity beta","Crypto volatility","USD exposure","Duration"],"Contribution":[26,22,19,12,8]}),hide_index=True,use_container_width=True,column_config={"Contribution":st.column_config.ProgressColumn("Contribution",min_value=0,max_value=30,format="%d")}); st.markdown("</div>",unsafe_allow_html=True)
    
    elif page == "Strategies":
        st.markdown('<div class="hero"><div class="smallcaps">STRATEGY LAB</div><h1>Strategies</h1><div class="hero-sub">Define systematic strategies before simulation, backtesting or paper execution.</div></div>',unsafe_allow_html=True)
        l,r=st.columns([1.2,.8])
        with l:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Strategy builder</div><div class="panel-subtitle">Configuration workspace</div></div>',unsafe_allow_html=True)
            x,y=st.columns(2)
            with x: signal=st.selectbox("Signal family",["Momentum","Mean Reversion","Macro","Multi-Factor"]); rebalance=st.selectbox("Rebalance",["Daily","Weekly","Monthly"])
            with y: risk_model=st.selectbox("Risk model",["Volatility Target","Risk Parity","Fixed Risk","Adaptive"]); execution=st.selectbox("Execution",["Paper","Backtest","Simulation"])
            st.slider("Target annualized volatility",5,25,12,1); st.slider("Maximum position weight",5,40,20,1); st.button("Build strategy specification",type="primary"); st.markdown("</div>",unsafe_allow_html=True)
        with r:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Strategy state</div><div class="panel-subtitle">Selected configuration</div></div>',unsafe_allow_html=True)
            for name,val in [("Signal",signal),("Risk model",risk_model),("Rebalance",rebalance),("Execution",execution)]: st.markdown(f'<div class="feed"><div class="feed-title">{name}</div><div class="feed-meta">{val}</div></div>',unsafe_allow_html=True)
            st.markdown("</div>",unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({"Strategy":["Global Momentum","Risk Parity","Trend + Macro","Adaptive Allocation"],"State":["READY","DESIGN","DESIGN","RESEARCH"],"Target Vol":["12%","10%","14%","DYNAMIC"],"Next":["Historical data","Risk model","Macro factors","Signal research"]}),hide_index=True,use_container_width=True)
    
    elif page == "Replay Lab":
        if "market_streams" not in st.session_state:
            from market_engine import seed_ohlcv
            st.session_state.market_streams = {
                symbol: seed_ohlcv(symbol, bars=240, seed=17)
                for symbol in ["SPX", "NDX", "BTC", "GOLD", "BRENT", "EURUSD"]
            }
        replay_symbol = st.selectbox(
            "Replay instrument",
            ["SPX", "NDX", "BTC", "GOLD", "BRENT", "EURUSD"],
            key="replay_symbol",
        )
        render_replay_lab(st.session_state.market_streams[replay_symbol], replay_symbol)

    elif page == "Backtesting":
        st.markdown('<div class="hero"><div class="smallcaps">QUANT RESEARCH</div><h1>Backtesting</h1><div class="hero-sub">Research strategies against historical data with costs, slippage and risk metrics.</div></div>',unsafe_allow_html=True)
        a,b,c,d=st.columns(4); a.metric("CAGR","14.8%","Demo"); b.metric("Sharpe","1.31","Demo"); c.metric("Max Drawdown","-11.4%","Demo"); d.metric("Win Rate","58.2%","Demo")
        l,r=st.columns([1.5,.7])
        with l:
            curve=pd.DataFrame({"Strategy":100*np.cumprod(1+rng.normal(.0008,.012,len(dates))),"Benchmark":100*np.cumprod(1+rng.normal(.0005,.010,len(dates)))},index=dates)
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Backtest equity curve</div><div class="panel-subtitle">Demonstration result</div></div>',unsafe_allow_html=True); st.line_chart(curve,height=350,use_container_width=True); st.markdown("</div>",unsafe_allow_html=True)
        with r:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Run configuration</div><div class="panel-subtitle">Future engine inputs</div></div>',unsafe_allow_html=True)
            st.selectbox("Strategy",["Global Momentum","Risk Parity","Trend + Macro"]); st.selectbox("Universe",["Global Equities","Multi-Asset","Crypto + Equities"]); st.select_slider("Period",options=["1Y","3Y","5Y","10Y"],value="5Y"); st.number_input("Transaction cost (bps)",min_value=0,max_value=100,value=5); st.button("Run backtest",type="primary"); st.markdown("</div>",unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({"Metric":["CAGR","Volatility","Sharpe","Sortino","Max Drawdown","VaR 95%"],"Strategy":["14.8%","12.3%","1.31","1.86","-11.4%","-2.7%"],"Benchmark":["11.2%","15.1%","0.94","1.33","-18.9%","-3.5%"]}),hide_index=True,use_container_width=True)
    
    elif page == "Execution":
        st.markdown('<div class="hero"><div class="smallcaps">ORDER MANAGEMENT</div><h1>Execution</h1><div class="hero-sub">Paper execution control room. Live routing remains disabled.</div></div>',unsafe_allow_html=True)
        st.warning("PAPER / SIMULATION ONLY — no live broker orders are connected.")
        l,r=st.columns([1,1.25])
        with l:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Order staging</div><div class="panel-subtitle">No live submission</div></div>',unsafe_allow_html=True)
            st.text_input("Asset","SPY"); st.number_input("Quantity",min_value=0.0,value=10.0,step=1.0); st.selectbox("Side",["BUY","SELL"]); st.selectbox("Order type",["MARKET","LIMIT","STOP"]); st.number_input("Limit / trigger price",min_value=0.0,value=0.0,step=.01); st.button("Stage paper order",type="primary"); st.markdown("</div>",unsafe_allow_html=True)
        with r:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Order blotter</div><div class="panel-subtitle">Demonstration history</div></div>',unsafe_allow_html=True)
            st.dataframe(pd.DataFrame({"Time":["09:42","10:18","11:07","11:32"],"Asset":["SPY","BTC","GLD","QQQ"],"Side":["BUY","BUY","SELL","BUY"],"Qty":[12,.025,8,6],"Status":["SIMULATED","SIMULATED","SIMULATED","STAGED"]}),hide_index=True,use_container_width=True); st.markdown("</div>",unsafe_allow_html=True)
        st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Execution pipeline</div><div class="panel-subtitle">Target architecture</div></div>',unsafe_allow_html=True)
        cols=st.columns(8)
        for col,stage in zip(cols,["Signal","Risk check","Position check","Order validation","Broker adapter","Fill","Portfolio update","Audit"]):
            with col: st.markdown(f'<div class="matrix-cell"><div class="matrix-name">{stage.upper()}</div><div class="matrix-value flat">READY</div></div>',unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="hero"><div class="smallcaps">MONITORING</div><h1>Alerts</h1><div class="hero-sub">Market, portfolio and AI event monitoring.</div></div>',unsafe_allow_html=True)
        a,b,c=st.columns(3); a.metric("Open Alerts","3","+1 today"); b.metric("Acknowledged","5","This week"); c.metric("Rules Active","7","Demo")
        l,r=st.columns([1.3,.7])
        with l:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Alert feed</div><div class="panel-subtitle">Latest events</div></div>',unsafe_allow_html=True)
            st.dataframe(pd.DataFrame({"Severity":["MEDIUM","LOW","LOW","INFO"],"Alert":["Technology concentration above target","Gold momentum improving","Volatility normalizing","Portfolio rebalance window approaching"],"State":["OPEN","OPEN","ACKNOWLEDGED","OPEN"]}),hide_index=True,use_container_width=True); st.markdown("</div>",unsafe_allow_html=True)
        with r:
            st.markdown('<div class="panel"><div class="panel-header"><div class="panel-title">Alert rules</div><div class="panel-subtitle">Monitoring switches</div></div>',unsafe_allow_html=True)
            st.checkbox("Drawdown threshold",True); st.checkbox("Volatility regime change",True); st.checkbox("Concentration threshold",True); st.checkbox("AI anomaly detection",False); st.checkbox("Macro event monitor",True); st.markdown("</div>",unsafe_allow_html=True)
    
    st.markdown('<div style="height:.7rem"></div><div class="muted2" style="font-size:.61rem;text-align:right">FINSIGHT GLOBAL · TERMINAL UI v0.3 · DEMONSTRATION DATA ONLY</div>',unsafe_allow_html=True)
    

render_finsight_app()
