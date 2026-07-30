from quant.oanda_data import _candles_to_df

SAMPLE_CANDLES = [
    {
        "time": "2024-01-01T00:00:00.000000000Z",
        "complete": True,
        "volume": 120,
        "mid": {"o": "1.10500", "h": "1.10600", "l": "1.10400", "c": "1.10550"},
    },
    {
        "time": "2024-01-01T01:00:00.000000000Z",
        "complete": True,
        "volume": 95,
        "mid": {"o": "1.10550", "h": "1.10650", "l": "1.10500", "c": "1.10600"},
    },
    {
        # in-progress candle from OANDA must be dropped
        "time": "2024-01-01T02:00:00.000000000Z",
        "complete": False,
        "volume": 10,
        "mid": {"o": "1.10600", "h": "1.10620", "l": "1.10590", "c": "1.10610"},
    },
]


def test_candles_to_df_drops_incomplete_and_parses_types():
    df = _candles_to_df(SAMPLE_CANDLES)

    assert len(df) == 2
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert df["close"].iloc[0] == 1.10550
    assert df["volume"].dtype.kind == "i"
    assert df.index.is_monotonic_increasing


def test_candles_to_df_empty_input():
    df = _candles_to_df([])
    assert df.empty
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
