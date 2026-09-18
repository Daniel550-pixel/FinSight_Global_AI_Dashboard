from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..market.order_book import OrderBook
from ..execution.simulator import ExecutionSimulator


@dataclass
class QuantState:
    position: float = 0.0
    cash: float = 100_000.0
    realized_pnl: float = 0.0
    last_price: float | None = None
    events_processed: int = 0


@dataclass
class QuantPipeline:
    """Connects market state, strategy signals and paper execution."""

    initial_cash: float = 100_000.0
    max_position: float = 100.0
    executor: ExecutionSimulator = field(default_factory=ExecutionSimulator)

    def __post_init__(self) -> None:
        self.state = QuantState(cash=float(self.initial_cash))
        self.book = OrderBook()

    def on_bar(self, event: Any) -> dict:
        payload = event.payload or {}
        price = float(event.price or payload.get("close", 0.0))
        self.state.last_price = price
        self.state.events_processed += 1

        signal = self._signal(event)
        fills = []
        if signal and abs(self.state.position) < self.max_position:
            qty = min(1.0, self.max_position - abs(self.state.position))
            order_id = self.executor.submit(event.symbol, signal, qty)
            fills = self.executor.process_bar(
                symbol=event.symbol,
                timestamp_ns=event.timestamp_ns,
                open_price=float(payload.get("open", price)),
                high=float(payload.get("high", price)),
                low=float(payload.get("low", price)),
                close=price,
            )
            for fill in fills:
                signed_qty = fill.quantity if fill.side == "buy" else -fill.quantity
                self.state.position += signed_qty
                self.state.cash -= signed_qty * fill.price
                self.state.cash -= fill.fee
                self.state.realized_pnl -= fill.fee

        return {
            "signal": signal or "hold",
            "price": price,
            "position": self.state.position,
            "cash": self.state.cash,
            "fills": fills,
            "order_id": order_id if signal else None,
        }

    def _signal(self, event: Any) -> str | None:
        payload = event.payload or {}
        open_price = float(payload.get("open", event.price or 0.0))
        close = float(payload.get("close", event.price or 0.0))
        if close > open_price * 1.003:
            return "buy"
        if close < open_price * 0.997:
            return "sell"
        return None

    def snapshot(self) -> dict:
        equity = self.state.cash
        if self.state.last_price is not None:
            equity += self.state.position * self.state.last_price
        return {
            "position": self.state.position,
            "cash": self.state.cash,
            "last_price": self.state.last_price,
            "realized_pnl": self.state.realized_pnl,
            "equity": equity,
            "events_processed": self.state.events_processed,
            "open_orders": len(self.executor.orders),
            "fills": len(self.executor.fills),
        }
