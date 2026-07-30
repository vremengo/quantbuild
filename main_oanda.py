import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from quant.backtest import run_backtest
from quant.metrics import compute_metrics
from quant.oanda_data import fetch_eurusd_oanda
from quant.strategy import moving_average_crossover


def main():
    df = fetch_eurusd_oanda(start="2023-01-01", granularity="H1")
    signal = moving_average_crossover(df, fast=50, slow=200)
    result = run_backtest(df, signal, spread_pips=1.0)
    metrics = compute_metrics(result)

    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")

    result["equity"].plot(title="EUR/USD (OANDA H1) MA Crossover Strategy - Equity Curve")
    plt.savefig("equity_curve_oanda.png")
    print("Saved chart to equity_curve_oanda.png")


if __name__ == "__main__":
    main()
