from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class BookLevel:
    price: float
    quantity: float


@dataclass
class OrderBook:
    """Deterministic L2 order-book state used by replay and simulation."""

    bids: dict[float, float] = field(default_factory=dict)
    asks: dict[float, float] = field(default_factory=dict)
    sequence: int = 0
    timestamp_ns: int = 0

    def apply_snapshot(
        self,
        bids: Iterable[tuple[float, float]],
        asks: Iterable[tuple[float, float]],
        *,
        timestamp_ns: int = 0,
        sequence: int | None = None,
    ) -> None:
        self.bids = {float(p): float(q) for p, q in bids if q > 0}
        self.asks = {float(p): float(q) for p, q in asks if q > 0}
        self._advance(timestamp_ns, sequence)

    def update(
        self,
        side: str,
        price: float,
        quantity: float,
        *,
        timestamp_ns: int = 0,
        sequence: int | None = None,
    ) -> None:
        book = self.bids if side.lower() == "bid" else self.asks
        price = float(price)
        quantity = float(quantity)
        if quantity <= 0:
            book.pop(price, None)
        else:
            book[price] = quantity
        self._advance(timestamp_ns, sequence)

    def best_bid(self) -> BookLevel | None:
        return self._best(self.bids, reverse=True)

    def best_ask(self) -> BookLevel | None:
        return self._best(self.asks, reverse=False)

    def mid_price(self) -> float | None:
        bid, ask = self.best_bid(), self.best_ask()
        if not bid or not ask:
            return None
        return (bid.price + ask.price) / 2.0

    def spread(self) -> float | None:
        bid, ask = self.best_bid(), self.best_ask()
        if not bid or not ask:
            return None
        return ask.price - bid.price

    def microprice(self) -> float | None:
        bid, ask = self.best_bid(), self.best_ask()
        if not bid or not ask:
            return None
        total = bid.quantity + ask.quantity
        if total <= 0:
            return None
        return (ask.price * bid.quantity + bid.price * ask.quantity) / total

    def depth(self, levels: int = 10) -> dict[str, list[BookLevel]]:
        return {
            "bids": [BookLevel(p, self.bids[p]) for p in sorted(self.bids, reverse=True)[:levels]],
            "asks": [BookLevel(p, self.asks[p]) for p in sorted(self.asks)[:levels]],
        }

    def imbalance(self, levels: int = 5) -> float:
        d = self.depth(levels)
        bid_qty = sum(x.quantity for x in d["bids"])
        ask_qty = sum(x.quantity for x in d["asks"])
        total = bid_qty + ask_qty
        return 0.0 if total <= 0 else (bid_qty - ask_qty) / total

    def queue_ahead(self, side: str, price: float) -> float:
        """Approximate displayed quantity ahead at the order's price level."""
        book = self.bids if side.lower() == "buy" else self.asks
        return max(0.0, float(book.get(float(price), 0.0)))

    def snapshot(self, levels: int = 10) -> dict:
        d = self.depth(levels)
        return {
            "timestamp_ns": self.timestamp_ns,
            "sequence": self.sequence,
            "best_bid": d["bids"][0].__dict__ if d["bids"] else None,
            "best_ask": d["asks"][0].__dict__ if d["asks"] else None,
            "mid": self.mid_price(),
            "spread": self.spread(),
            "microprice": self.microprice(),
            "imbalance": self.imbalance(min(levels, 5)),
            "bids": [x.__dict__ for x in d["bids"]],
            "asks": [x.__dict__ for x in d["asks"]],
        }

    def _advance(self, timestamp_ns: int, sequence: int | None) -> None:
        self.timestamp_ns = int(timestamp_ns)
        if sequence is None:
            self.sequence += 1
        else:
            self.sequence = int(sequence)

    @staticmethod
    def _best(book: dict[float, float], reverse: bool) -> BookLevel | None:
        if not book:
            return None
        price = sorted(book, reverse=reverse)[0]
        return BookLevel(price, book[price])
