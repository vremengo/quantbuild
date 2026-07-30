import os

import pandas as pd
import requests

OANDA_INSTRUMENT = "EUR_USD"
MAX_CANDLES_PER_REQUEST = 5000

BASE_URLS = {
    "practice": "https://api-fxpractice.oanda.com",
    "live": "https://api-fxtrade.oanda.com",
}


def _get_session() -> tuple[requests.Session, str]:
    token = os.environ.get("OANDA_API_TOKEN")
    if not token:
        raise RuntimeError(
            "OANDA_API_TOKEN environment variable is not set. "
            "Create a practice account at oanda.com, generate a personal "
            "access token under Manage API Access, then run:\n"
            "  export OANDA_API_TOKEN=your-token-here"
        )
    environment = os.environ.get("OANDA_ENVIRONMENT", "practice")
    if environment not in BASE_URLS:
        raise ValueError(f"OANDA_ENVIRONMENT must be 'practice' or 'live', got {environment!r}")

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session, BASE_URLS[environment]


def _candles_to_df(candles: list[dict]) -> pd.DataFrame:
    rows = [
        {
            "time": c["time"],
            "open": float(c["mid"]["o"]),
            "high": float(c["mid"]["h"]),
            "low": float(c["mid"]["l"]),
            "close": float(c["mid"]["c"]),
            "volume": int(c["volume"]),
        }
        for c in candles
        if c["complete"]
    ]
    df = pd.DataFrame(rows, columns=["time", "open", "high", "low", "close", "volume"])
    df["time"] = pd.to_datetime(df["time"])
    return df.set_index("time")


def fetch_eurusd_oanda(start: str, end: str | None = None, granularity: str = "H1") -> pd.DataFrame:
    """Fetch EUR/USD mid-price candles from OANDA, paginating past the 5000-candle limit."""
    session, base_url = _get_session()
    url = f"{base_url}/v3/instruments/{OANDA_INSTRUMENT}/candles"

    start_dt = pd.Timestamp(start, tz="UTC")
    end_dt = pd.Timestamp(end, tz="UTC") if end else pd.Timestamp.now(tz="UTC")

    frames = []
    cursor = start_dt
    while cursor < end_dt:
        params = {
            "granularity": granularity,
            "price": "M",
            "from": cursor.isoformat(),
            "to": end_dt.isoformat(),
            "count": MAX_CANDLES_PER_REQUEST,
        }
        response = session.get(url, params=params, timeout=30)
        response.raise_for_status()
        candles = response.json()["candles"]
        if not candles:
            break

        df = _candles_to_df(candles)
        if df.empty:
            break
        frames.append(df)
        cursor = df.index[-1] + pd.Timedelta(seconds=1)

        if len(candles) < MAX_CANDLES_PER_REQUEST:
            break

    if not frames:
        return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])

    return pd.concat(frames).sort_index()
