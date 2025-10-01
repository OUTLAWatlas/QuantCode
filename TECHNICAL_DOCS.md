# QUANTCODE - Technical Documentation

## Overview
QUANTCODE is a professional Python-based trading analysis tool that implements Heiken Ashi candle analysis to generate decisive trading signals. The core function `analyze_heiken_ashi()` provides BUY/SELL/HOLD signals based on precise mathematical calculations and candle pattern recognition.

## Core Function: `analyze_heiken_ashi(ticker: str) -> dict`

### Parameters
- **ticker** (str): Stock ticker symbol (e.g., "AAPL", "RELIANCE.NS")

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

## Heiken Ashi Calculation

The function implements the following precise formulas:

1. **HA_Close** = (Open + High + Low + Close) / 4
2. **HA_Open** = (Previous HA_Open + Previous HA_Close) / 2
3. **HA_High** = MAX(Current High, HA_Open, HA_Close)
4. **HA_Low** = MIN(Current Low, HA_Open, HA_Close)

## Signal Generation Logic

### BUY Signal
- **Condition**: Bullish candle (HA_Close > HA_Open) AND no lower wick (HA_Open == HA_Low)
- **Interpretation**: Strong upward momentum with no selling pressure at the bottom

### SELL Signal
- **Condition**: Bearish candle (HA_Close < HA_Open) AND no upper wick (HA_Open == HA_High)
- **Interpretation**: Strong downward momentum with no buying pressure at the top

### HOLD Signal
- **Condition**: All other scenarios
- **Interpretation**: Indecisive market conditions, wait for clearer signals

## Technical Features

### Data Source
- **Provider**: Yahoo Finance via `yfinance` library
- **Period**: Last 100 days of historical data
- **Frequency**: Daily candlesticks

### Error Handling
- Invalid ticker symbols
- Network connectivity issues
- Insufficient data validation
- Input parameter validation

### Performance Optimizations
- Efficient pandas DataFrame operations
- Minimal memory footprint
- Fast mathematical calculations
- Proper column indexing for multi-ticker support

## Installation & Dependencies

```bash
pip install pandas yfinance
```

## Usage Examples

### Basic Usage
```python
from quantcode_analyzer import analyze_heiken_ashi

result = analyze_heiken_ashi("AAPL")
print(f"Signal: {result['signal']}")
print(f"Price: ${result['latest_close_price']:.2f}")
```

### Portfolio Screening
```python
portfolio = ["AAPL", "TSLA", "MSFT"]
for ticker in portfolio:
    result = analyze_heiken_ashi(ticker)
    if result['signal'] == 'BUY':
        print(f"BUY opportunity: {ticker}")
```

### Error Handling
```python
try:
    result = analyze_heiken_ashi("INVALID_TICKER")
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## File Structure

```
QuantCode/
├── quantcode_analyzer.py    # Core analysis function
├── test_analyzer.py         # Comprehensive test suite
├── examples.py              # Usage examples and patterns
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
└── LICENSE                 # License information
```

## Market Coverage

### Supported Markets
- **US Stocks**: AAPL, TSLA, MSFT, GOOGL, AMZN, etc.
- **Indian Stocks**: RELIANCE.NS, TCS.NS, INFY.NS, etc.
- **International**: Most Yahoo Finance supported tickers

### Ticker Format Examples
- US: `AAPL`, `TSLA`, `MSFT`
- India: `RELIANCE.NS`, `TCS.NS`
- UK: `TSCO.L`, `BP.L`
- Canada: `SHOP.TO`, `RY.TO`

## Algorithm Validation

### Mathematical Accuracy
- Precise implementation of Heiken Ashi formulas
- Floating-point arithmetic with epsilon comparison
- Iterative calculation for sequential dependencies

### Signal Reliability
- Based on established technical analysis principles
- Clear, unambiguous decision rules
- No subjective interpretation required

## Performance Characteristics

### Speed
- Average execution time: 1-3 seconds per ticker
- Efficient pandas operations
- Minimal API calls to data provider

### Memory Usage
- Low memory footprint
- Streaming calculations where possible
- Automatic garbage collection

### Reliability
- Robust error handling
- Network timeout management
- Data validation at multiple levels

## Production Considerations

### Scalability
- Suitable for individual ticker analysis
- Can be wrapped for batch processing
- Consider rate limiting for large-scale usage

### Monitoring
- Built-in error reporting
- Logging capabilities can be added
- Performance metrics tracking ready

### Security
- No sensitive data storage
- Read-only market data access
- Safe input validation

## Disclaimer

This tool is for educational and analytical purposes only. Trading signals should not be considered as financial advice. Always conduct your own research and consider consulting with financial professionals before making investment decisions.

---

**Version**: 1.0.0  
**Last Updated**: October 2025  
**Author**: QuantCode Team