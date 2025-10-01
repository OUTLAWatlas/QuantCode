"""
QUANTCODE Trading Analysis Application
=====================================

A professional trading analysis tool that implements Heiken Ashi candle analysis
and identifies decisive trading signals for stock market analysis.

Author: QuantCode Team
Date: October 2025
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Union


def analyze_heiken_ashi(ticker: str) -> Dict[str, Union[str, float]]:
    """
    Analyze a stock using Heiken Ashi candles and generate decisive trading signals.
    
    This function fetches the last 100 days of historical data for a given ticker,
    calculates Heiken Ashi candles, and generates BUY/SELL/HOLD signals based on
    the most recent candle's characteristics.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "RELIANCE.NS", "AAPL")
        
    Returns:
        Dict[str, Union[str, float]]: Dictionary containing:
            - ticker: The input ticker symbol
            - signal: Trading signal ("BUY", "SELL", or "HOLD")
            - strategy: Strategy name ("Heiken Ashi Decisive Candle")
            - latest_close_price: Most recent closing price
            
    Raises:
        ValueError: If ticker is invalid or data cannot be fetched
        Exception: For other unexpected errors during processing
        
    Examples:
        >>> result = analyze_heiken_ashi("RELIANCE.NS")
        >>> print(result)
        {
            "ticker": "RELIANCE.NS",
            "signal": "BUY",
            "strategy": "Heiken Ashi Decisive Candle",
            "latest_close_price": 2456.75
        }
    """
    
    try:
        # Validate input
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Ticker must be a non-empty string")
        
        # Fetch last 100 days of historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=100)
        
        # Download data with error handling
        data = yf.download(
            ticker, 
            start=start_date, 
            end=end_date, 
            progress=False,
            auto_adjust=True,
            prepost=True
        )
        
        # Flatten column headers if they are multi-level (when single ticker)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)
        
        # Validate data was retrieved
        if data.empty:
            raise ValueError(f"No data found for ticker '{ticker}'. Please check the ticker symbol.")
        
        if len(data) < 2:
            raise ValueError(f"Insufficient data for ticker '{ticker}'. Need at least 2 days of data.")
        
        # Store the latest close price for return value
        latest_close_price = data['Close'].iloc[-1]
        
        # Calculate Heiken Ashi candles using proper pandas indexing
        n = len(data)
        ha_data = pd.DataFrame(index=data.index, 
                              columns=['HA_Open', 'HA_High', 'HA_Low', 'HA_Close'],
                              dtype=float)
        
        # Calculate HA_Close for all candles first
        ha_data['HA_Close'] = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        
        # Initialize first HA_Open
        ha_data.loc[data.index[0], 'HA_Open'] = (data['Open'].iloc[0] + data['Close'].iloc[0]) / 2
        
        # Calculate HA_Open for subsequent candles using iterative approach
        for i in range(1, n):
            prev_idx = data.index[i-1]
            curr_idx = data.index[i]
            ha_data.loc[curr_idx, 'HA_Open'] = (
                ha_data.loc[prev_idx, 'HA_Open'] + ha_data.loc[prev_idx, 'HA_Close']
            ) / 2
        
        # Calculate HA_High and HA_Low for all candles
        for i in range(n):
            idx = data.index[i]
            ha_data.loc[idx, 'HA_High'] = max(
                data['High'].iloc[i],
                ha_data.loc[idx, 'HA_Open'],
                ha_data.loc[idx, 'HA_Close']
            )
            ha_data.loc[idx, 'HA_Low'] = min(
                data['Low'].iloc[i],
                ha_data.loc[idx, 'HA_Open'],
                ha_data.loc[idx, 'HA_Close']
            )
        
        # Generate trading signal based on the latest (most recent) Heiken Ashi candle
        latest_ha = ha_data.iloc[-1]
        
        ha_open = latest_ha['HA_Open']
        ha_close = latest_ha['HA_Close']
        ha_high = latest_ha['HA_High']
        ha_low = latest_ha['HA_Low']
        
        # Apply decisive signal generation rules
        if ha_close > ha_open:  # Bullish candle
            # BUY Signal: Bullish candle with no lower wick (HA_Open == HA_Low)
            if abs(ha_open - ha_low) < 1e-10:  # Using small epsilon for float comparison
                signal = "BUY"
            else:
                signal = "HOLD"
        elif ha_close < ha_open:  # Bearish candle
            # SELL Signal: Bearish candle with no upper wick (HA_Open == HA_High)
            if abs(ha_open - ha_high) < 1e-10:  # Using small epsilon for float comparison
                signal = "SELL"
            else:
                signal = "HOLD"
        else:  # ha_close == ha_open (Doji candle)
            signal = "HOLD"
        
        # Return formatted result
        result = {
            "ticker": ticker,
            "signal": signal,
            "strategy": "Heiken Ashi Decisive Candle",
            "latest_close_price": latest_close_price
        }
        
        return result
        
    except ValueError as ve:
        # Handle validation and data-related errors
        raise ValueError(str(ve))
    except Exception as e:
        # Handle any unexpected errors
        raise Exception(f"Error analyzing ticker {ticker}: {str(e)}")


if __name__ == "__main__":
    # Example usage and testing
    test_tickers = ["RELIANCE.NS", "AAPL", "TSLA"]
    
    print("QUANTCODE Trading Analysis")
    print("=" * 50)
    
    for ticker in test_tickers:
        try:
            result = analyze_heiken_ashi(ticker)
            print(f"\nTicker: {result['ticker']}")
            print(f"Signal: {result['signal']}")
            print(f"Strategy: {result['strategy']}")
            print(f"Latest Close: ${result['latest_close_price']:.2f}")
        except Exception as e:
            print(f"\nError analyzing {ticker}: {e}")