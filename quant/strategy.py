import pandas as pd


def moving_average_crossover(df: pd.DataFrame, fast: int = 50, slow: int = 200) -> pd.Series:
    fast_ma = df["close"].rolling(fast).mean()
    slow_ma = df["close"].rolling(slow).mean()

    signal = pd.Series(0, index=df.index)
    signal[fast_ma > slow_ma] = 1
    signal[fast_ma < slow_ma] = -1
    return signal
