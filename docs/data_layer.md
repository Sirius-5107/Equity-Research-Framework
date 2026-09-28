# Data Layer

The data layer is the foundation of the framework:

Universe -> Market Data -> Cleaning -> Factors

## Universe

equity_research.data.universe loads the current NIFTY 500 constituent file
from the NSE archive and normalizes symbols independently from data vendors.

## Market data

equity_research.data.market_data.download_ohlcv downloads historical OHLCV
data from Yahoo Finance and returns a deterministic tidy schema:

Date, Symbol, Open, High, Low, Close, Adj Close, Volume

The downloader preserves Close and Adj Close separately so downstream
research can explicitly choose the appropriate price series.

## Cleaning

The cleaning module contains small, reusable transformations. Median
imputation is intentionally opt-in and should not be used blindly for
time-series market data.

## Migration notes

Migrated from the Summer-Project data pipeline:

- retained the tidy OHLCV representation;
- retained NSE .NS symbol handling;
- retained batch Yahoo Finance downloads;
- removed CLI/output concerns from the reusable library;
- removed the stale NIFTY 50 hard-coded fallback from the core NIFTY 500 path;
- moved generic cleaning into tested library functions;
- did not migrate generated CSVs, notebooks, cached bytecode, or strategy-specific logic.
