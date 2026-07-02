# Multi-Crypto Event-Driven Trading System

End-to-end multi-cryptocurrency trading research and backtesting framework using Binance public REST API data.

## Run order

1. `notebooks/01_download_binance_data.ipynb`
2. `notebooks/02_clean_and_engineer_features.ipynb`
3. `notebooks/03_strategy_signals.ipynb`
4. `notebooks/04_order_book_and_matching_engine.ipynb`
5. `notebooks/05_event_driven_backtester.ipynb`
6. `notebooks/06_binance_testnet_template.ipynb`

Important: extract the ZIP to a normal folder, not the Windows temp ZIP preview folder.

## What it does

- Downloads 5-minute OHLCV data for BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, and XRPUSDT.
- Cleans and caches raw/feature datasets in Parquet.
- Engineers momentum, moving-average, volatility, volume, and cross-sectional rank features.
- Implements a modular strategy class.
- Implements simplified order management, order book, matching engine, execution fees, slippage, and partial fills.
- Runs an event-driven portfolio backtest and saves trades/performance reports.

## Suggested resume bullet

Built a modular multi-crypto event-driven trading and backtesting framework using Binance REST API data, cross-sectional momentum features, simulated order book execution, portfolio risk controls, and performance analytics in Python.
