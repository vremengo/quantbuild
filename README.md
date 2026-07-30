# quantbuild

Starter EUR/USD backtesting project. Fetches daily EUR/USD prices, runs a
moving-average crossover strategy, and reports basic performance metrics.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

This fetches EUR/USD data via `yfinance`, runs the strategy, prints metrics
(total return, annualized return/vol, Sharpe ratio, max drawdown), and saves
an equity curve chart to `equity_curve.png`.

## Test

```bash
pip install pytest
pytest tests/
```

Tests run against synthetic price data, so they work without network access.

## Project layout

```
quant/
  data.py      # fetches EUR/USD price data
  strategy.py  # moving-average crossover signal
  backtest.py  # turns signal into positions, PnL, equity curve (spread-aware)
  metrics.py   # total return, Sharpe ratio, max drawdown
main.py        # ties it all together
tests/         # pipeline tests on synthetic data
```

## Next steps

- Swap `quant/data.py` for a broker API (OANDA, Interactive Brokers) once you
  want intraday data or live/paper trading.
- Try different strategies in `quant/strategy.py` — signal functions just
  need to return a `pandas.Series` of `-1`/`0`/`1`.
- Tune `fast`/`slow`/`spread_pips` and compare metrics before trusting any
  result — a single backtest run proves nothing on its own.
