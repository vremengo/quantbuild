import pandas as pd
import yfinance as yf

EURUSD_TICKER = "EURUSD=X"


def fetch_eurusd(start: str, end: str | None = None, interval: str = "1d") -> pd.DataFrame:
    df = yf.download(EURUSD_TICKER, start=start, end=end, interval=interval, auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns=str.lower)
    df = df.dropna()
    return df
