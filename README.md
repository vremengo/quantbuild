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

## OANDA (intraday data)

`quant/oanda_data.py` fetches EUR/USD candles directly from the OANDA v20
REST API (no extra SDK — just `requests`), for intraday granularities
`yfinance` doesn't reliably provide.

1. Create a free practice account: https://www.oanda.com/register/#/sign-up/demo
2. Generate a personal access token: **My Account → Manage API Access**
3. Set it as an environment variable (never commit it):
   ```bash
   export OANDA_API_TOKEN=your-token-here
   # export OANDA_ENVIRONMENT=practice   # default; use "live" for a real account
   ```
4. Run the OANDA-backed backtest:
   ```bash
   python main_oanda.py
   ```

`fetch_eurusd_oanda(start, end=None, granularity="H1")` returns the same
`open/high/low/close/volume` DataFrame shape as `quant/data.py`, so it drops
straight into the existing `strategy`/`backtest`/`metrics` pipeline. It
paginates automatically past OANDA's 5000-candles-per-request limit.

## Project layout

```
quant/
  data.py        # fetches daily EUR/USD data via yfinance
  oanda_data.py  # fetches intraday EUR/USD candles via the OANDA REST API
  strategy.py    # moving-average crossover signal
  backtest.py    # turns signal into positions, PnL, equity curve (spread-aware)
  metrics.py     # total return, Sharpe ratio, max drawdown
main.py          # runs the pipeline against yfinance data
main_oanda.py    # runs the pipeline against OANDA data
tests/           # pipeline tests on synthetic data
```

## Next steps

- Try different strategies in `quant/strategy.py` — signal functions just
  need to return a `pandas.Series` of `-1`/`0`/`1`.
- Tune `fast`/`slow`/`spread_pips` and compare metrics before trusting any
  result — a single backtest run proves nothing on its own.
- Once a strategy looks solid on historical data, OANDA's same API supports
  placing orders on the practice account for paper trading.
