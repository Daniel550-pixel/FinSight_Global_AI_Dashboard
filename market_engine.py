import numpy as np
import pandas as pd


def seed_ohlcv(symbol: str, bars: int = 240, seed: int = 17) -> pd.DataFrame:
    """Create an OHLCV market stream for UI simulation."""
    profiles = {
        "SPX": (6481.2, 0.00010, 0.0100),
        "NDX": (23914.6, 0.00016, 0.0120),
        "BTC": (113420.0, 0.00022, 0.0200),
        "GOLD": (3812.4, 0.00008, 0.0100),
        "BRENT": (68.7, -0.00002, 0.0160),
        "EURUSD": (1.174, 0.00003, 0.0060),
    }
    price, drift, volatility = profiles.get(symbol, (100.0, 0.0001, 0.012))
    rng = np.random.default_rng(seed + abs(hash(symbol)) % 1000)

    regimes = np.zeros(bars)
    regime = 1.0
    for i in range(bars):
        if i > 20 and rng.random() < 0.035:
            regime *= -1
        regimes[i] = regime

    shocks = rng.normal(0.0, volatility, bars)
    returns = drift * regimes + shocks
    close = price * np.cumprod(1 + returns)

    open_ = np.empty(bars)
    open_[0] = close[0] / (1 + returns[0])
    open_[1:] = close[:-1]

    intraday = np.maximum(0.001, np.abs(rng.normal(volatility * 0.42, volatility * 0.12, bars)))
    high = np.maximum(open_, close) * (1 + intraday)
    low = np.minimum(open_, close) * (1 - intraday)
    volume = rng.integers(8_000, 90_000, bars) * (1 + np.abs(returns) * 25)

    idx = pd.date_range(
        end=pd.Timestamp.now().floor("min"),
        periods=bars,
        freq="5min",
    )
    return pd.DataFrame(
        {"Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume.astype(int)},
        index=idx,
    )


def advance_ohlcv(frame: pd.DataFrame, seed: int = 17) -> pd.DataFrame:
    """Advance the simulation by one 5-minute bar."""
    rng = np.random.default_rng(seed + len(frame) * 7)
    prev = float(frame["Close"].iloc[-1])
    vol = float(frame["Close"].pct_change().rolling(30).std().iloc[-1])
    vol = 0.012 if not np.isfinite(vol) or vol <= 0 else float(np.clip(vol, 0.003, 0.04))
    shock = float(rng.normal(0.00015, vol))
    close = prev * (1 + shock)
    open_ = prev
    spread = max(abs(shock), vol * 0.25)
    high = max(open_, close) * (1 + abs(rng.normal(0, spread * 0.35)))
    low = min(open_, close) * (1 - abs(rng.normal(0, spread * 0.35)))
    volume = int(max(5_000, rng.integers(10_000, 75_000) * (1 + abs(shock) * 30)))
    next_index = frame.index[-1] + pd.Timedelta(minutes=5)
    row = pd.DataFrame(
        {"Open": [open_], "High": [high], "Low": [low], "Close": [close], "Volume": [volume]},
        index=[next_index],
    )
    return pd.concat([frame, row]).tail(240)


def add_indicators(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    close = df["Close"]
    high = df["High"]
    low = df["Low"]

    df["SMA20"] = close.rolling(20).mean()
    df["SMA50"] = close.rolling(50).mean()
    df["EMA12"] = close.ewm(span=12, adjust=False).mean()
    df["EMA26"] = close.ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["MACDSignal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACDHist"] = df["MACD"] - df["MACDSignal"]

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["RSI14"] = 100 - (100 / (1 + rs))

    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)
    df["ATR14"] = tr.rolling(14).mean()
    df["ATRpct"] = df["ATR14"] / close * 100

    df["RollingHigh20"] = high.rolling(20).max().shift(1)
    df["RollingLow20"] = low.rolling(20).min().shift(1)
    df["VolumeMA20"] = df["Volume"].rolling(20).mean()

    df["Return1"] = close.pct_change() * 100
    df["Return20"] = close.pct_change(20) * 100
    return df


def classify_candlestick(df: pd.DataFrame) -> str:
    row = df.iloc[-1]
    body = abs(row["Close"] - row["Open"])
    rng = max(row["High"] - row["Low"], 1e-12)
    upper = row["High"] - max(row["Open"], row["Close"])
    lower = min(row["Open"], row["Close"]) - row["Low"]

    if body / rng < 0.12 and lower / rng > 0.55:
        return "Hammer"
    if body / rng < 0.12 and upper / rng > 0.55:
        return "Shooting star"
    if row["Close"] > row["Open"] and body / rng > 0.65:
        return "Strong bullish candle"
    if row["Close"] < row["Open"] and body / rng > 0.65:
        return "Strong bearish candle"
    return "Neutral candle"


def analyze_market(df: pd.DataFrame) -> dict:
    x = add_indicators(df)
    row = x.iloc[-1]

    score = 0
    reasons = []

    if row["SMA20"] > row["SMA50"]:
        score += 22
        reasons.append("20-period trend is above the 50-period trend.")
    else:
        score -= 22
        reasons.append("20-period trend is below the 50-period trend.")

    if row["Close"] > row["SMA20"]:
        score += 14
        reasons.append("Price is holding above the short-term trend.")
    else:
        score -= 14
        reasons.append("Price is below the short-term trend.")

    if row["MACD"] > row["MACDSignal"]:
        score += 18
        reasons.append("MACD momentum is positive.")
    else:
        score -= 18
        reasons.append("MACD momentum is negative.")

    rsi = float(row["RSI14"]) if np.isfinite(row["RSI14"]) else 50.0
    if rsi >= 58:
        score += 12
        reasons.append("RSI confirms positive momentum.")
    elif rsi <= 42:
        score -= 12
        reasons.append("RSI confirms negative momentum.")
    else:
        reasons.append("RSI is neutral.")

    candle = classify_candlestick(x)
    if candle == "Strong bullish candle":
        score += 10
        reasons.append("Latest candle shows strong buying pressure.")
    elif candle == "Strong bearish candle":
        score -= 10
        reasons.append("Latest candle shows strong selling pressure.")
    elif candle == "Hammer":
        score += 5
        reasons.append("Hammer pattern may indicate rejection of lower prices.")
    elif candle == "Shooting star":
        score -= 5
        reasons.append("Shooting-star pattern may indicate rejection of higher prices.")

    if np.isfinite(row["RollingHigh20"]) and row["Close"] > row["RollingHigh20"]:
        score += 12
        reasons.append("Price is breaking above the 20-bar range.")
    elif np.isfinite(row["RollingLow20"]) and row["Close"] < row["RollingLow20"]:
        score -= 12
        reasons.append("Price is breaking below the 20-bar range.")

    score = int(np.clip(score, -100, 100))
    if score >= 40:
        regime = "BULLISH"
    elif score <= -40:
        regime = "BEARISH"
    else:
        regime = "NEUTRAL"

    if score >= 55:
        action = "PAPER BUY"
    elif score <= -55:
        action = "PAPER SELL"
    else:
        action = "HOLD"

    confidence = int(np.clip(55 + abs(score) * 0.42, 55, 95))
    volatility = float(row["ATRpct"]) if np.isfinite(row["ATRpct"]) else 0.0

    return {
        "score": score,
        "regime": regime,
        "action": action,
        "confidence": confidence,
        "rsi": rsi,
        "atr_pct": volatility,
        "pattern": candle,
        "macd": float(row["MACD"]),
        "macd_signal": float(row["MACDSignal"]),
        "price": float(row["Close"]),
        "volume_ratio": float(row["Volume"] / row["VolumeMA20"]) if row["VolumeMA20"] else 1.0,
        "reasons": reasons[-5:],
        "data": x,
    }
