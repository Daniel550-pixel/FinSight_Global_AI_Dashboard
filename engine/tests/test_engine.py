import pandas as pd

from engine.execution.simulator import ExecutionSimulator
from engine.market.order_book import OrderBook
from engine.replay.session import MarketEvent, ReplaySession
from engine.quant.pipeline import QuantPipeline


def test_order_book_state():
    book = OrderBook()
    book.apply_snapshot([(100, 5), (99, 10)], [(101, 4), (102, 8)], timestamp_ns=1)
    assert book.best_bid().price == 100
    assert book.best_ask().price == 101
    assert book.mid_price() == 100.5
    assert book.imbalance(2) > 0


def test_limit_order_fill():
    sim = ExecutionSimulator(fee_bps=0, slippage_bps=0)
    order_id = sim.submit("TEST", "buy", 2, price=100, order_type="limit")
    fills = sim.process_bar(symbol="TEST", timestamp_ns=2, open_price=102, high=103, low=99, close=101)
    assert fills[0].order_id == order_id
    assert fills[0].price == 100
    assert not sim.orders


def test_replay_is_deterministic():
    events = [
        MarketEvent(3, "bar", "TEST", price=101, payload={"open": 100, "high": 102, "low": 99, "close": 101}),
        MarketEvent(1, "bar", "TEST", price=100, payload={"open": 99, "high": 101, "low": 98, "close": 100}),
    ]
    session = ReplaySession(events)
    assert [e.timestamp_ns for e in session.events] == [1, 3]

    pipeline = QuantPipeline(initial_cash=1000)
    results = []
    session.replay(lambda event: results.append(pipeline.on_bar(event)))
    assert len(results) == 2
    assert pipeline.snapshot()["events_processed"] == 2


def test_ohlcv_replay_roundtrip(tmp_path):
    frame = pd.DataFrame(
        {
            "Open": [100.0, 100.0],
            "High": [101.0, 102.0],
            "Low": [99.0, 99.0],
            "Close": [100.5, 101.5],
            "Volume": [10, 20],
        },
        index=pd.date_range("2026-01-01", periods=2, freq="5min"),
    )
    session = ReplaySession.from_ohlcv(frame, "TEST")
    path = session.to_json(tmp_path / "session.json")
    restored = ReplaySession.from_json(path)
    assert len(restored) == 2
    assert restored.events[1].price == 101.5
