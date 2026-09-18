"""FinSight Replay Lab — Streamlit visualization layer over the deterministic replay engine.

This module intentionally contains UI only. ReplaySession, QuantPipeline and ExecutionSimulator
remain Streamlit-independent so the same session data can later drive live, batch and AI workflows.
"""

import pandas as pd
import streamlit as st

from engine.replay.session import ReplaySession
from engine.quant.pipeline import QuantPipeline


@st.cache_data(show_spinner=False)
def build_replay_session(frame: pd.DataFrame, symbol: str) -> ReplaySession:
    """Cache immutable replay construction so navigation does not rebuild the event log."""
    return ReplaySession.from_ohlcv(frame.tail(240), symbol=symbol)


def render_replay_lab(frame: pd.DataFrame, symbol: str) -> None:
    st.markdown(
        '<div class="hero"><div class="smallcaps">QUANT RESEARCH / REPLAY</div>'
        '<h1>Replay Lab</h1>'
        '<div class="hero-sub">Deterministic market replay, strategy state and simulated execution — separated from UI rendering.</div></div>',
        unsafe_allow_html=True,
    )

    session = build_replay_session(frame, symbol)
    pipeline = QuantPipeline(initial_cash=100_000, max_position=100)

    start = session.start_ns
    end = session.end_ns
    if start is None or end is None:
        st.info("No replayable market events are available for this instrument.")
        return

    total_seconds = max((end - start) / 1_000_000_000, 1.0)
    cursor_seconds = st.slider(
        "Replay position",
        min_value=0.0,
        max_value=float(total_seconds),
        value=float(total_seconds),
        step=max(total_seconds / 240.0, 1.0),
        format="%.0f s",
    )
    replay_end = start + int(cursor_seconds * 1_000_000_000)

    processed = session.replay(pipeline.on_bar, end_ns=replay_end)
    state = pipeline.snapshot()
    replay_events = [event for event in session.events if event.timestamp_ns <= replay_end]
    last_event = replay_events[-1] if replay_events else None

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Events", f"{state['events_processed']:,}")
    m2.metric("Position", f"{state['position']:.2f}")
    m3.metric("Cash", f"USD {state['cash']:,.2f}")
    m4.metric("Equity", f"USD {state['equity']:,.2f}")
    m5.metric("Open orders", str(len(state["open_orders"])))

    left, right = st.columns([1.35, .85])
    with left:
        st.markdown(
            '<div class="panel"><div class="panel-header"><div class="panel-title">Replay timeline</div>'
            f'<div class="panel-subtitle">{symbol} · {len(session):,} events · deterministic ordering</div></div>',
            unsafe_allow_html=True,
        )
        visible = frame.tail(120).copy()
        st.line_chart(visible["Close"], height=360, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div class="panel"><div class="panel-header"><div class="panel-title">Quant state</div>'
            '<div class="panel-subtitle">Strategy → execution → portfolio</div></div>',
            unsafe_allow_html=True,
        )
        for name, value in [
            ("Replay start", pd.to_datetime(start, unit="ns").strftime("%Y-%m-%d %H:%M:%S")),
            ("Replay cursor", pd.to_datetime(replay_end, unit="ns").strftime("%Y-%m-%d %H:%M:%S")),
            ("Last price", f"USD {state['last_price']:,.4f}" if state["last_price"] else "—"),
            ("Realized P/L", f"USD {state['realized_pnl']:,.2f}"),
            ("Last event", last_event.event_type if last_event else "—"),
        ]:
            st.markdown(
                f'<div class="feed"><div class="feed-title">{name}</div>'
                f'<div class="feed-meta">{value}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    fills = pd.DataFrame(
        [
            {
                "Order": fill.order_id,
                "Symbol": fill.symbol,
                "Side": fill.side.upper(),
                "Quantity": fill.quantity,
                "Price": fill.price,
                "Fee": fill.fee,
                "Timestamp": pd.to_datetime(fill.timestamp_ns, unit="ns").strftime("%H:%M:%S"),
            }
            for fill in pipeline.executor.fills
        ]
    )
    st.markdown(
        '<div class="panel"><div class="panel-header"><div class="panel-title">Execution ledger</div>'
        '<div class="panel-subtitle">Simulated fills produced during replay</div></div>',
        unsafe_allow_html=True,
    )
    if fills.empty:
        st.caption("No simulated fills have occurred at the selected replay position.")
    else:
        st.dataframe(fills, hide_index=True, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
