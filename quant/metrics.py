import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


def compute_metrics(result: pd.DataFrame) -> dict:
    returns = result["strategy_returns"]
    equity = result["equity"]

    total_return = equity.iloc[-1] - 1
    annualized_return = (1 + total_return) ** (TRADING_DAYS_PER_YEAR / len(returns)) - 1
    annualized_vol = returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
    sharpe_ratio = annualized_return / annualized_vol if annualized_vol != 0 else float("nan")

    running_max = equity.cummax()
    drawdown = equity / running_max - 1
    max_drawdown = drawdown.min()

    return {
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_vol": annualized_vol,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
    }
