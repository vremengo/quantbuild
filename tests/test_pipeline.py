import numpy as np
import pandas as pd

from quant.backtest import run_backtest
from quant.metrics import compute_metrics
from quant.strategy import moving_average_crossover


def make_synthetic_prices(n: int = 800, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2020-01-01", periods=n, freq="B")
    returns = rng.normal(0, 0.005, n)
    price = 1.10 * (1 + returns).cumprod()
    return pd.DataFrame({"close": price}, index=dates)


def test_pipeline_runs_end_to_end():
    df = make_synthetic_prices()
    signal = moving_average_crossover(df, fast=50, slow=200)
    result = run_backtest(df, signal, spread_pips=1.0)
    metrics = compute_metrics(result)

    assert len(result) == len(df)
    assert set(["total_return", "annualized_return", "annualized_vol", "sharpe_ratio", "max_drawdown"]) <= metrics.keys()
    assert np.isfinite(result["equity"]).all()


def test_signal_has_no_lookahead():
    df = make_synthetic_prices()
    signal = moving_average_crossover(df, fast=50, slow=200)
    result = run_backtest(df, signal)
    # position at bar t must equal signal at bar t-1, never bar t
    assert (result["position"].iloc[1:].values == signal.shift(1).fillna(0).iloc[1:].values).all()
