"""
QUANTCODE Trading Analysis Application - Flask API Ready
========================================================

A professional trading analysis class that implements multiple technical analysis
strategies and provides structured data for API consumption.

Author: QuantCode Team
Date: October 2025
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Union, List, Optional
import warnings

# Suppress pandas warnings
warnings.filterwarnings('ignore')


class QuantCodeAnalyzer:
    """
    Advanced trading analysis class implementing multiple technical indicators
    and providing consolidated trading signals suitable for Flask API usage.
    """
    
    def __init__(self, ticker: str, days: int = 100):
        """
        Initialize the analyzer with a ticker symbol and data period.
        
        Args:
            ticker (str): Stock ticker symbol (e.g., "AAPL", "RELIANCE.NS")
            days (int): Number of days of historical data to fetch (default: 100)
        """
        self.ticker = ticker
        self.days = days
        self.data = None
        self.latest_close_price = None
        
    def _fetch_data(self) -> bool:
        """
        Fetch historical data for the ticker.
        
        Returns:
            bool: True if data fetched successfully, False otherwise
        """
        try:
            # Validate input
            if not self.ticker or not isinstance(self.ticker, str):
                raise ValueError("Ticker must be a non-empty string")
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.days)
            
            # Download data
            self.data = yf.download(
                self.ticker,
                start=start_date,
                end=end_date,
                progress=False,
                auto_adjust=True,
                prepost=True
            )
            
            # Flatten column headers if multi-level
            if isinstance(self.data.columns, pd.MultiIndex):
                self.data.columns = self.data.columns.droplevel(1)
            
            # Validate data
            if self.data.empty:
                raise ValueError(f"No data found for ticker '{self.ticker}'")
            
            if len(self.data) < 20:  # Need minimum data for technical indicators
                raise ValueError(f"Insufficient data for ticker '{self.ticker}'. Need at least 20 days.")
            
            # Store latest close price
            self.latest_close_price = float(self.data['Close'].iloc[-1])
            
            return True
            
        except Exception as e:
            raise Exception(f"Error fetching data for {self.ticker}: {str(e)}")
    
    def analyze_heiken_ashi(self) -> Dict[str, Union[str, float, Dict]]:
        """
        Analyze using Heiken Ashi candles and generate trading signals.
        
        Returns:
            Dict containing signal, details, and additional information
        """
        try:
            if self.data is None:
                self._fetch_data()
            
            n = len(self.data)
            ha_data = pd.DataFrame(
                index=self.data.index,
                columns=['HA_Open', 'HA_High', 'HA_Low', 'HA_Close'],
                dtype=float
            )
            
            # Calculate HA_Close for all candles
            ha_data['HA_Close'] = (
                self.data['Open'] + self.data['High'] + 
                self.data['Low'] + self.data['Close']
            ) / 4
            
            # Initialize first HA_Open
            ha_data.loc[self.data.index[0], 'HA_Open'] = (
                self.data['Open'].iloc[0] + self.data['Close'].iloc[0]
            ) / 2
            
            # Calculate HA_Open for subsequent candles
            for i in range(1, n):
                prev_idx = self.data.index[i-1]
                curr_idx = self.data.index[i]
                ha_data.loc[curr_idx, 'HA_Open'] = (
                    ha_data.loc[prev_idx, 'HA_Open'] + 
                    ha_data.loc[prev_idx, 'HA_Close']
                ) / 2
            
            # Calculate HA_High and HA_Low
            for i in range(n):
                idx = self.data.index[i]
                ha_data.loc[idx, 'HA_High'] = max(
                    self.data['High'].iloc[i],
                    ha_data.loc[idx, 'HA_Open'],
                    ha_data.loc[idx, 'HA_Close']
                )
                ha_data.loc[idx, 'HA_Low'] = min(
                    self.data['Low'].iloc[i],
                    ha_data.loc[idx, 'HA_Open'],
                    ha_data.loc[idx, 'HA_Close']
                )
            
            # Analyze latest candle
            latest_ha = ha_data.iloc[-1]
            ha_open = latest_ha['HA_Open']
            ha_close = latest_ha['HA_Close']
            ha_high = latest_ha['HA_High']
            ha_low = latest_ha['HA_Low']
            
            # Generate signal
            if ha_close > ha_open:  # Bullish candle
                if abs(ha_open - ha_low) < 1e-10:  # No lower wick
                    signal = "BUY"
                    details = "Decisive Bullish Candle - Strong upward momentum"
                else:
                    signal = "HOLD"
                    details = "Bullish candle with lower wick - Mixed signals"
            elif ha_close < ha_open:  # Bearish candle
                if abs(ha_open - ha_high) < 1e-10:  # No upper wick
                    signal = "SELL"
                    details = "Decisive Bearish Candle - Strong downward momentum"
                else:
                    signal = "HOLD"
                    details = "Bearish candle with upper wick - Mixed signals"
            else:  # Doji candle
                signal = "HOLD"
                details = "Doji candle - Market indecision"
            
            return {
                "signal": signal,
                "details": details,
                "candle_type": "Bullish" if ha_close > ha_open else "Bearish" if ha_close < ha_open else "Doji",
                "ha_values": {
                    "open": float(ha_open),
                    "high": float(ha_high),
                    "low": float(ha_low),
                    "close": float(ha_close)
                }
            }
            
        except Exception as e:
            return {
                "signal": "HOLD",
                "details": f"Error in Heiken Ashi analysis: {str(e)}",
                "error": True
            }
    
    def analyze_bollinger_bands(self, window: int = 20, std_dev: int = 2) -> Dict[str, Union[str, float, Dict]]:
        """
        Analyze using Bollinger Bands.
        
        Args:
            window (int): Moving average period (default: 20)
            std_dev (int): Standard deviation multiplier (default: 2)
            
        Returns:
            Dict containing signal, details, and band values
        """
        try:
            if self.data is None:
                self._fetch_data()
            
            # Calculate Bollinger Bands
            close_prices = self.data['Close']
            sma = close_prices.rolling(window=window).mean()
            std = close_prices.rolling(window=window).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            # Get latest values
            latest_close = close_prices.iloc[-1]
            latest_upper = upper_band.iloc[-1]
            latest_lower = lower_band.iloc[-1]
            latest_sma = sma.iloc[-1]
            
            # Calculate position within bands
            band_width = latest_upper - latest_lower
            position_pct = (latest_close - latest_lower) / band_width * 100
            
            # Generate signal
            if latest_close > latest_upper:
                signal = "SELL"
                details = f"Price above upper band ({position_pct:.1f}%) - Overbought"
            elif latest_close < latest_lower:
                signal = "BUY"
                details = f"Price below lower band ({position_pct:.1f}%) - Oversold"
            elif latest_close > latest_sma:
                signal = "HOLD"
                details = f"Price above SMA ({position_pct:.1f}%) - Bullish bias"
            else:
                signal = "HOLD"
                details = f"Price below SMA ({position_pct:.1f}%) - Bearish bias"
            
            return {
                "signal": signal,
                "details": details,
                "position_percent": round(position_pct, 2),
                "band_values": {
                    "upper": float(latest_upper),
                    "middle": float(latest_sma),
                    "lower": float(latest_lower),
                    "current_price": float(latest_close)
                }
            }
            
        except Exception as e:
            return {
                "signal": "HOLD",
                "details": f"Error in Bollinger Bands analysis: {str(e)}",
                "error": True
            }
    
    def analyze_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, Union[str, float, Dict]]:
        """
        Analyze using MACD (Moving Average Convergence Divergence).
        
        Args:
            fast (int): Fast EMA period (default: 12)
            slow (int): Slow EMA period (default: 26)
            signal (int): Signal line EMA period (default: 9)
            
        Returns:
            Dict containing signal, details, and MACD values
        """
        try:
            if self.data is None:
                self._fetch_data()
            
            # Calculate MACD
            close_prices = self.data['Close']
            ema_fast = close_prices.ewm(span=fast).mean()
            ema_slow = close_prices.ewm(span=slow).mean()
            
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal).mean()
            histogram = macd_line - signal_line
            
            # Get latest values
            latest_macd = macd_line.iloc[-1]
            latest_signal = signal_line.iloc[-1]
            latest_histogram = histogram.iloc[-1]
            prev_histogram = histogram.iloc[-2] if len(histogram) > 1 else 0
            
            # Generate signal
            if latest_macd > latest_signal and prev_histogram <= 0:
                signal_result = "BUY"
                details = "MACD crossed above Signal line - Bullish crossover"
            elif latest_macd < latest_signal and prev_histogram >= 0:
                signal_result = "SELL"
                details = "MACD crossed below Signal line - Bearish crossover"
            elif latest_macd > latest_signal:
                signal_result = "HOLD"
                details = "MACD above Signal line - Bullish momentum"
            else:
                signal_result = "HOLD"
                details = "MACD below Signal line - Bearish momentum"
            
            return {
                "signal": signal_result,
                "details": details,
                "trend": "Bullish" if latest_macd > latest_signal else "Bearish",
                "macd_values": {
                    "macd": float(latest_macd),
                    "signal_line": float(latest_signal),
                    "histogram": float(latest_histogram)
                }
            }
            
        except Exception as e:
            return {
                "signal": "HOLD",
                "details": f"Error in MACD analysis: {str(e)}",
                "error": True
            }
    
    def analyze_rsi(self, window: int = 14) -> Dict[str, Union[str, float, Dict]]:
        """
        Analyze using RSI (Relative Strength Index).
        
        Args:
            window (int): RSI calculation period (default: 14)
            
        Returns:
            Dict containing signal, details, and RSI value
        """
        try:
            if self.data is None:
                self._fetch_data()
            
            # Calculate RSI
            close_prices = self.data['Close']
            delta = close_prices.diff()
            
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            latest_rsi = rsi.iloc[-1]
            
            # Generate signal
            if latest_rsi > 70:
                signal = "SELL"
                details = f"RSI {latest_rsi:.1f} - Overbought condition"
            elif latest_rsi < 30:
                signal = "BUY"
                details = f"RSI {latest_rsi:.1f} - Oversold condition"
            elif latest_rsi > 50:
                signal = "HOLD"
                details = f"RSI {latest_rsi:.1f} - Bullish momentum"
            else:
                signal = "HOLD"
                details = f"RSI {latest_rsi:.1f} - Bearish momentum"
            
            return {
                "signal": signal,
                "details": details,
                "rsi_value": round(float(latest_rsi), 2),
                "condition": "Overbought" if latest_rsi > 70 else "Oversold" if latest_rsi < 30 else "Neutral"
            }
            
        except Exception as e:
            return {
                "signal": "HOLD",
                "details": f"Error in RSI analysis: {str(e)}",
                "error": True
            }
    
    def get_final_signal(self) -> Dict[str, Union[str, float, Dict]]:
        """
        Perform comprehensive analysis using all indicators and return consolidated signal.
        
        Returns:
            Dict containing ticker, final_signal, and all individual analyses
        """
        try:
            # Ensure data is fetched
            if self.data is None:
                self._fetch_data()
            
            # Perform all analyses
            heiken_ashi_result = self.analyze_heiken_ashi()
            bollinger_result = self.analyze_bollinger_bands()
            macd_result = self.analyze_macd()
            rsi_result = self.analyze_rsi()
            
            # Collect all signals
            signals = [
                heiken_ashi_result.get('signal', 'HOLD'),
                bollinger_result.get('signal', 'HOLD'),
                macd_result.get('signal', 'HOLD'),
                rsi_result.get('signal', 'HOLD')
            ]
            
            # Count signal votes
            buy_votes = signals.count('BUY')
            sell_votes = signals.count('SELL')
            hold_votes = signals.count('HOLD')
            
            # Determine final signal based on majority voting
            if buy_votes >= 2 and buy_votes > sell_votes:
                final_signal = "BUY"
                confidence = f"{buy_votes}/4 indicators agree"
            elif sell_votes >= 2 and sell_votes > buy_votes:
                final_signal = "SELL"
                confidence = f"{sell_votes}/4 indicators agree"
            else:
                final_signal = "HOLD"
                confidence = "Mixed signals - no clear consensus"
            
            # Return comprehensive result
            return {
                "ticker": self.ticker,
                "final_signal": final_signal,
                "confidence": confidence,
                "latest_close_price": self.latest_close_price,
                "analyses": {
                    "heiken_ashi": heiken_ashi_result,
                    "bollinger_bands": bollinger_result,
                    "macd": macd_result,
                    "rsi": rsi_result
                },
                "signal_summary": {
                    "buy_votes": buy_votes,
                    "sell_votes": sell_votes,
                    "hold_votes": hold_votes,
                    "total_indicators": 4
                }
            }
            
        except Exception as e:
            return {
                "ticker": self.ticker,
                "final_signal": "HOLD",
                "error": str(e),
                "analyses": {},
                "confidence": "Error in analysis"
            }


# Standalone function for backward compatibility
def analyze_heiken_ashi(ticker: str) -> Dict[str, Union[str, float]]:
    """
    Backward compatible function for Heiken Ashi analysis only.
    
    Args:
        ticker (str): Stock ticker symbol
        
    Returns:
        Dict containing basic Heiken Ashi analysis results
    """
    try:
        analyzer = QuantCodeAnalyzer(ticker)
        ha_result = analyzer.analyze_heiken_ashi()
        
        return {
            "ticker": ticker,
            "signal": ha_result["signal"],
            "strategy": "Heiken Ashi Decisive Candle",
            "latest_close_price": analyzer.latest_close_price
        }
        
    except Exception as e:
        raise Exception(f"Error analyzing ticker {ticker}: {str(e)}")


if __name__ == "__main__":
    # Example usage and testing
    test_tickers = ["AAPL", "RELIANCE.NS", "TSLA"]
    
    print("QUANTCODE Trading Analysis - Multi-Indicator")
    print("=" * 60)
    
    for ticker in test_tickers:
        try:
            analyzer = QuantCodeAnalyzer(ticker)
            result = analyzer.get_final_signal()
            
            print(f"\n📊 Analysis for {result['ticker']}:")
            print(f"💰 Latest Price: ${result['latest_close_price']:.2f}")
            print(f"🎯 Final Signal: {result['final_signal']}")
            print(f"📈 Confidence: {result['confidence']}")
            
            print("\n📋 Individual Indicators:")
            for indicator, analysis in result['analyses'].items():
                signal_emoji = "📈" if analysis['signal'] == 'BUY' else "📉" if analysis['signal'] == 'SELL' else "⏸️"
                print(f"   {signal_emoji} {indicator.replace('_', ' ').title()}: {analysis['signal']} - {analysis['details']}")
                
        except Exception as e:
            print(f"\nError analyzing {ticker}: {e}")