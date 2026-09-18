from __future__ import annotations

from dataclasses import dataclass, field
from itertools import count


@dataclass(frozen=True)
class Fill:
    order_id: int
    timestamp_ns: int
    symbol: str
    side: str
    price: float
    quantity: float
    fee: float


@dataclass
class _Order:
    order_id: int
    symbol: str
    side: str
    quantity: float
    price: float | None
    remaining: float


class ExecutionSimulator:
    """Paper execution layer with explicit slippage and fees."""

    def __init__(self, fee_bps: float = 1.0, slippage_bps: float = 2.0) -> None:
        self.fee_bps = max(0.0, float(fee_bps))
        self.slippage_bps = max(0.0, float(slippage_bps))
        self._ids = count(1)
        self.orders: dict[int, _Order] = {}
        self.fills: list[Fill] = []

    def submit(
        self,
        symbol: str,
        side: str,
        quantity: float,
        *,
        price: float | None = None,
        order_type: str = "market",
    ) -> int:
        side = side.lower()
        order_type = order_type.lower()
        if side not in {"buy", "sell"}:
            raise ValueError("side must be buy or sell")
        if order_type not in {"market", "limit"}:
            raise ValueError("order_type must be market or limit")
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if order_type == "limit" and price is None:
            raise ValueError("limit orders require a price")
        order_id = next(self._ids)
        self.orders[order_id] = _Order(order_id, symbol, side, float(quantity), price, float(quantity))
        return order_id

    def process_bar(
        self,
        *,
        symbol: str,
        timestamp_ns: int,
        open_price: float,
        high: float,
        low: float,
        close: float,
    ) -> list[Fill]:
        fills: list[Fill] = []
        for order in list(self.orders.values()):
            if order.symbol != symbol or order.remaining <= 0:
                continue

            execution_price = self._execution_price(order, open_price, high, low, close)
            if execution_price is None:
                continue

            notional = execution_price * order.remaining
            fee = notional * self.fee_bps / 10_000
            fill = Fill(
                order_id=order.order_id,
                timestamp_ns=int(timestamp_ns),
                symbol=symbol,
                side=order.side,
                price=execution_price,
                quantity=order.remaining,
                fee=fee,
            )
            fills.append(fill)
            self.fills.append(fill)
            order.remaining = 0.0
            del self.orders[order.order_id]
        return fills

    def cancel(self, order_id: int) -> bool:
        return self.orders.pop(order_id, None) is not None

    def _execution_price(self, order: _Order, open_price: float, high: float, low: float, close: float) -> float | None:
        if order.price is None:
            return self._slipped(open_price, order.side)
        if order.side == "buy" and low <= order.price:
            return float(order.price)
        if order.side == "sell" and high >= order.price:
            return float(order.price)
        return None

    def _slipped(self, price: float, side: str) -> float:
        factor = self.slippage_bps / 10_000
        return float(price * (1 + factor if side == "buy" else 1 - factor))
