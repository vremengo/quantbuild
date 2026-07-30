import pandas as pd

PIP = 0.0001


def run_backtest(df: pd.DataFrame, signal: pd.Series, spread_pips: float = 1.0) -> pd.DataFrame:
    price = df["close"]
    returns = price.pct_change().fillna(0)

    # trade on the bar after the signal fires, never on the same bar it was computed on
    position = signal.shift(1).fillna(0)

    trade_opened = position.diff().fillna(position).ne(0)
    spread_cost = trade_opened * (spread_pips * PIP / price)

    strategy_returns = position * returns - spread_cost
    equity = (1 + strategy_returns).cumprod()

    return pd.DataFrame(
        {
            "close": price,
            "position": position,
            "returns": returns,
            "strategy_returns": strategy_returns,
            "equity": equity,
        }
    )
