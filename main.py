import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from quant.backtest import run_backtest
from quant.data import fetch_eurusd
from quant.metrics import compute_metrics
from quant.strategy import moving_average_crossover


def main():
    df = fetch_eurusd(start="2010-01-01")
    signal = moving_average_crossover(df, fast=50, slow=200)
    result = run_backtest(df, signal, spread_pips=1.0)
    metrics = compute_metrics(result)

    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")

    result["equity"].plot(title="EUR/USD MA Crossover Strategy - Equity Curve")
    plt.savefig("equity_curve.png")
    print("Saved chart to equity_curve.png")


if __name__ == "__main__":
    main()
