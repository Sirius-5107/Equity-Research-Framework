# Data Layer

The data layer is the foundation of the framework:
Universe -> Market Data -> Cleaning -> Factors

## Universe

`equity_research.data.universe` loads the current NIFTY 500 constituent file
from the NSE archive and normalizes symbols independently from data vendors.

For historical backtests, the current constituent list must **not** be projected
backward. That creates survivorship bias. Use `equity_research.data.pit` with a
point-in-time membership history, or an input dataset that already contains an
explicit PIT constituent flag.

The membership adapter expects half-open intervals:
`[valid_from, valid_to)`

A null `valid_to` means the membership interval is still open.

Example:

```python
from equity_research.data.pit import apply_pit_membership, load_membership_history

membership = load_membership_history(
    "data/nifty500_membership_history.csv",
    index_name="Nifty 500",
)
prices_pit = apply_pit_membership(prices, membership)
```

One public source for the interval table is the `aditya-jha/nse-historical-membership`
dataset, which documents the schema, coverage, provenance, and known pre-2018
reconstruction gaps. Treat its coverage/source labels as part of the research
provenance rather than as ground truth. For higher-reliability studies, retain the
source version/date with the experiment.

## Market data

`equity_research.data.market_data.download_ohlcv` downloads historical OHLCV
data from Yahoo Finance and returns a deterministic tidy schema:

Date, Symbol, Open, High, Low, Close, Adj Close, Volume

The downloader preserves Close and Adj Close separately so downstream
research can explicitly choose the appropriate price series.

## Cleaning

The cleaning module contains small, reusable transformations. Median
imputation is intentionally opt-in and should not be used blindly for
time-series market data.
