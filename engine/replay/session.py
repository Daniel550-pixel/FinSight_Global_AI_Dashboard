from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Callable, Iterable


@dataclass(frozen=True)
class MarketEvent:
    timestamp_ns: int
    event_type: str
    symbol: str
    side: str | None = None
    price: float | None = None
    quantity: float | None = None
    sequence: int | None = None
    payload: dict | None = None

    @property
    def timestamp(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp_ns / 1_000_000_000, tz=timezone.utc)


class ReplaySession:
    """Immutable event-log session for deterministic market replay."""

    FORMAT = "FINSIGHT-REPLAY-1"

    def __init__(self, events: Iterable[MarketEvent] = ()) -> None:
        self._events = tuple(sorted(events, key=lambda e: (e.timestamp_ns, e.sequence or 0)))

    @property
    def events(self) -> tuple[MarketEvent, ...]:
        return self._events

    @property
    def start_ns(self) -> int | None:
        return self._events[0].timestamp_ns if self._events else None

    @property
    def end_ns(self) -> int | None:
        return self._events[-1].timestamp_ns if self._events else None

    def __len__(self) -> int:
        return len(self._events)

    def replay(
        self,
        handler: Callable[[MarketEvent], None],
        *,
        start_ns: int | None = None,
        end_ns: int | None = None,
    ) -> int:
        count = 0
        for event in self._events:
            if start_ns is not None and event.timestamp_ns < start_ns:
                continue
            if end_ns is not None and event.timestamp_ns > end_ns:
                break
            handler(event)
            count += 1
        return count

    def to_json(self, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "format": self.FORMAT,
            "event_count": len(self._events),
            "events": [asdict(event) for event in self._events],
        }
        target.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
        return target

    @classmethod
    def from_json(cls, path: str | Path) -> "ReplaySession":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if payload.get("format") != cls.FORMAT:
            raise ValueError("Unsupported FinSight replay format")
        return cls(MarketEvent(**event) for event in payload.get("events", []))

    @classmethod
    def from_ohlcv(cls, frame, symbol: str, interval_ns: int | None = None) -> "ReplaySession":
        events: list[MarketEvent] = []
        for i, (index, row) in enumerate(frame.iterrows()):
            timestamp_ns = int(index.value)
            events.append(
                MarketEvent(
                    timestamp_ns=timestamp_ns,
                    event_type="bar",
                    symbol=symbol,
                    price=float(row["Close"]),
                    quantity=float(row.get("Volume", 0.0)),
                    sequence=i,
                    payload={
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        "volume": float(row.get("Volume", 0.0)),
                        "interval_ns": interval_ns,
                    },
                )
            )
        return cls(events)
