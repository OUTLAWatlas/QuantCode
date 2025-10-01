# QUANTCODE Trading Analysis Application

A professional Python-based trading analysis tool that implements Heiken Ashi candle analysis and generates decisive trading signals.

## Features

- **Heiken Ashi Candle Calculation**: Implements precise mathematical formulas for smoothed candlestick analysis
- **Decisive Signal Generation**: Identifies clear BUY/SELL/HOLD signals based on candle characteristics
- **Robust Error Handling**: Comprehensive validation and error management for production use
- **Financial Data Integration**: Uses yfinance for reliable market data fetching

## Requirements

```
pandas
yfinance
```

## Usage

```python
from quantcode_analyzer import analyze_heiken_ashi

# Analyze a stock ticker
result = analyze_heiken_ashi("RELIANCE.NS")
print(result)
```

## Function Signature

```python
analyze_heiken_ashi(ticker: str) -> dict
```

### Parameters
- `ticker` (str): Stock ticker symbol (e.g., "RELIANCE.NS", "AAPL")

### Returns
Dictionary with the following structure:
```json
{
  "ticker": "TICKER_SYMBOL",
  "signal": "BUY" | "SELL" | "HOLD",
  "strategy": "Heiken Ashi Decisive Candle",
  "latest_close_price": 1234.56
}
```

## Trading Signal Logic

- **BUY**: Bullish candle (HA_Close > HA_Open) with no lower wick (HA_Open == HA_Low)
- **SELL**: Bearish candle (HA_Close < HA_Open) with no upper wick (HA_Open == HA_High)  
- **HOLD**: All other conditions

## Installation

1. Clone the repository
2. Install dependencies: `pip install pandas yfinance`
3. Run the analyzer: `python quantcode_analyzer.py`

## License

See LICENSE file for details.