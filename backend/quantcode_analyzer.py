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
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime, timedelta
from typing import Dict, Union, List, Optional
import warnings
import os

# Suppress pandas warnings
warnings.filterwarnings('ignore')


class QuantCodeAnalyzer:
	def get_final_signal(self, capital=5000, risk_percent=1, rr_ratio=3) -> Dict[str, Union[str, float, Dict]]:
		"""
		Generate the final trading signal and trade setup, including risk management.
		Args:
			capital (float): Total capital to risk
			risk_percent (float): Percent of capital to risk per trade
			rr_ratio (float): Risk-reward ratio for target
		Returns:
			Dict with signal, confidence, suggested stop loss, and trade setup
		"""
		try:
			if self.data is None:
				self._fetch_data()

			# Run all indicator analyses
			candle_patterns = self.analyze_candlestick_patterns()
			chart_patterns = self.analyze_chart_patterns()
			heiken_ashi_result = self.analyze_heiken_ashi()
			bollinger_result = self.analyze_bollinger_bands()
			macd_result = self.analyze_macd()
			divergence_result = self.analyze_divergence()
			rsi_result = self.analyze_rsi()
			primary_trend = self.analyze_primary_trend()

			# Aggregate scores for confluence
			total_score = sum([
				candle_patterns.get('score', 0),
				chart_patterns.get('score', 0),
				heiken_ashi_result.get('score', 0),
				bollinger_result.get('score', 0),
				macd_result.get('score', 0),
				divergence_result.get('score', 0)
			])

			# Determine final signal
			scores = {
				'BUY': 0,
				'SELL': 0,
				'HOLD': 0
			}
			for analysis in [candle_patterns, chart_patterns, heiken_ashi_result, bollinger_result, macd_result, divergence_result]:
				s = analysis.get('signal', 'HOLD')
				scores[s] += 1
			if scores['BUY'] > scores['SELL'] and scores['BUY'] > scores['HOLD']:
				final_signal = 'BUY'
			elif scores['SELL'] > scores['BUY'] and scores['SELL'] > scores['HOLD']:
				final_signal = 'SELL'
			else:
				final_signal = 'HOLD'

			# Confidence metric
			confidence = f"BUY:{scores['BUY']} SELL:{scores['SELL']} HOLD:{scores['HOLD']}"

			# Chart data for frontend
			chart_data = {
				'close': self._series_to_chart(self.data['Close']) if self.data is not None else [],
				'ema20': self._series_to_chart(self.ema20) if self.ema20 is not None else [],
				'ema50': self._series_to_chart(self.ema50) if self.ema50 is not None else [],
				'bb_upper': self._series_to_chart(self.bb_upper) if self.bb_upper is not None else [],
				'bb_lower': self._series_to_chart(self.bb_lower) if self.bb_lower is not None else [],
			}

			# --- Suggested Stop Loss ---
			suggested_stop_loss = None
			if final_signal == 'BUY':
				try:
					suggested_stop_loss = float(self.data['Low'].iloc[-1])
				except Exception:
					suggested_stop_loss = None
			elif final_signal == 'SELL':
				try:
					suggested_stop_loss = float(self.data['High'].iloc[-1])
				except Exception:
					suggested_stop_loss = None
			else:
				suggested_stop_loss = None

			# --- Trade Setup ---
			trade_setup = None
			if final_signal in ('BUY', 'SELL') and self.latest_close_price is not None and suggested_stop_loss is not None:
				entry_price = float(self.latest_close_price)
				stop_loss_price = float(suggested_stop_loss)
				risk_per_share = abs(entry_price - stop_loss_price)
				if risk_per_share == 0:
					position_size = 0
				else:
					position_size = int((capital * (risk_percent / 100)) / risk_per_share)
				if final_signal == 'BUY':
					target_price = entry_price + (risk_per_share * rr_ratio)
				else:
					target_price = entry_price - (risk_per_share * rr_ratio)
				trade_setup = {
					"entry_price": entry_price,
					"stop_loss_price": stop_loss_price,
					"risk_per_share": round(risk_per_share, 4),
					"target_price": round(target_price, 4),
					"position_size": position_size,
					"capital": capital,
					"risk_percent": risk_percent,
					"rr_ratio": rr_ratio,
					"suggested_stop_loss": suggested_stop_loss
				}

			return {
				"ticker": self.ticker,
				"final_signal": final_signal,
				"confidence": confidence,
				"latest_close_price": self.latest_close_price,
				"primary_trend": primary_trend,
				"total_score": total_score,
				"chart_data": chart_data,
				"suggested_stop_loss": suggested_stop_loss,
				"trade_setup": trade_setup,
				"analyses": {
					"candlestick_patterns": candle_patterns,
					"chart_patterns": chart_patterns,
					"heiken_ashi": heiken_ashi_result,
					"bollinger_bands": bollinger_result,
					"macd": macd_result,
					"divergence": divergence_result,
					"rsi": rsi_result
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
	"""
	Advanced trading analysis class implementing multiple technical indicators
	and providing consolidated trading signals suitable for Flask API usage.
	"""
    
	def __init__(self, ticker: str, days: int = 200):
		"""
		Initialize the analyzer with a ticker symbol and data period.
		Args:
			ticker (str): Stock ticker symbol (e.g., "AAPL", "RELIANCE.NS")
			days (int): Number of days of historical data to fetch (default: 200)
		"""
		self.ticker = ticker
		self.days = days
		self.data = None
		self.latest_close_price = None
		# Track fatal data-fetch/initialization errors
		self.error = None
		self.ema20 = None
		self.ema50 = None
		self.bb_upper = None
		self.bb_middle = None
		self.bb_lower = None
		self.macd_line = None
		self.macd_signal = None
		self.macd_hist = None
		self.rsi14 = None
		# Fetch data immediately
		self._fetch_data()
        

	def _fetch_data(self) -> bool:
		"""
		Fetch historical data for the ticker using Alpha Vantage.
		Returns:
			bool: True if data fetched successfully, False otherwise
		"""
		try:
			if not self.ticker or not isinstance(self.ticker, str):
				raise ValueError("Ticker must be a non-empty string")
			api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
			if not api_key:
				raise ValueError("Alpha Vantage API key not found in environment variables.")
			ts = TimeSeries(key=api_key, output_format='pandas')
			# Fetch daily adjusted data
			data, meta_data = ts.get_daily_adjusted(symbol=self.ticker, outputsize='compact')
			# Rename columns to match expected format
			rename_map = {
				'1. open': 'Open',
				'2. high': 'High',
				'3. low': 'Low',
				'4. close': 'Close',
				'6. volume': 'Volume'
			}
			data = data.rename(columns=rename_map)
			# Sort by date ascending
			data = data.sort_index()
			# Validate data
			if data.empty:
				raise ValueError(f"No data found for ticker '{self.ticker}' from Alpha Vantage.")
			if len(data) < 60:
				raise ValueError(f"Insufficient data for ticker '{self.ticker}'. Need at least 60 days.")
			self.data = data
			self.latest_close_price = float(self.data['Close'].iloc[-1])
			self._compute_indicators()
			return True
		except Exception as e:
			# Do not raise; record the error and return False so callers can handle gracefully
			self.error = f"Failed to fetch data: {e}"
			return False

	def _compute_indicators(self) -> None:
		"""Compute commonly used indicator series and store them as attributes.

		Safe to call multiple times; will recompute if data exists.
		"""
		if self.data is None or self.data.empty:
			return
		close = self.data['Close']
		# EMA 20 and EMA 50
		self.ema20 = close.ewm(span=20).mean()
		self.ema50 = close.ewm(span=50).mean()
		# Bollinger Bands (use 20-period SMA and 3 STD to align with analysis)
		sma20 = close.rolling(window=20).mean()
		std20 = close.rolling(window=20).std()
		self.bb_middle = sma20
		self.bb_upper = sma20 + 3 * std20
		self.bb_lower = sma20 - 3 * std20
		# MACD (12,26,9)
		ema_fast = close.ewm(span=12).mean()
		ema_slow = close.ewm(span=26).mean()
		macd_line = ema_fast - ema_slow
		macd_signal = macd_line.ewm(span=9).mean()
		self.macd_line = macd_line
		self.macd_signal = macd_signal
		self.macd_hist = macd_line - macd_signal
		# RSI 14 (SMA-based to match analyze_rsi)
		delta = close.diff()
		gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
		loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
		rs = gain / loss
		self.rsi14 = 100 - (100 / (1 + rs))

	def _ensure_indicators(self) -> None:
		"""Ensure indicator attributes are computed if missing and data exists."""
		if self.data is None:
			self._fetch_data()
		# If still missing any, compute
		if any(x is None for x in [self.ema20, self.ema50, self.bb_upper, self.bb_middle, self.bb_lower, self.macd_line, self.macd_signal, self.macd_hist, self.rsi14]):
			self._compute_indicators()

	@staticmethod
	def _to_date_str(idx_val) -> str:
		try:
			return idx_val.strftime('%Y-%m-%d')
		except Exception:
			s = str(idx_val)
			return s[:10]

	def _series_to_chart(self, series: pd.Series) -> List[Dict[str, Union[str, float]]]:
		"""Convert a pandas Series into a list of {time, value} dicts for charting."""
		if series is None is True:
			return []
		clean = series.dropna()
		return [{ 'time': self._to_date_str(idx), 'value': float(val) } for idx, val in clean.items()]
    
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
			score = 1 if signal == "BUY" else -1 if signal == "SELL" else 0

			return {
				"signal": signal,
				"score": score,
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
    
	def analyze_bollinger_bands(self, window: int = 20, std_dev: int = 3) -> Dict[str, Union[str, float, Dict]]:
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
			# Calculate position within bands
			band_width = latest_upper - latest_lower
			position_pct = (latest_close - latest_lower) / band_width * 100

			# Generate signal with 3SD extremes emphasis
			if latest_close > latest_upper:
				signal = "SELL"
				details = f"Close above 3SD upper band ({position_pct:.1f}%) - Extreme extension"
				score = -2
			elif latest_close < latest_lower:
				signal = "BUY"
				details = f"Close below 3SD lower band ({position_pct:.1f}%) - Extreme panic"
				score = +2
			else:
				signal = "HOLD"
				details = f"Within bands near {('above' if latest_close > sma.iloc[-1] else 'below')} SMA - Mean reversion likely"
				score = 0

			return {
				"signal": signal,
				"score": score,
				"details": details,
				"bands": {
					"upper": float(latest_upper),
					"lower": float(latest_lower),
					"sma": float(sma.iloc[-1])
				},
				"position_pct": round(position_pct, 2)
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
				score = +1
			elif latest_macd < latest_signal and prev_histogram >= 0:
				signal_result = "SELL"
				details = "MACD crossed below Signal line - Bearish crossover"
				score = -1
			elif latest_macd > latest_signal:
				signal_result = "HOLD"
				details = "MACD above Signal line - Bullish momentum"
				score = 0
			else:
				signal_result = "HOLD"
				details = "MACD below Signal line - Bearish momentum"
				score = 0
            
			return {
				"signal": signal_result,
				"score": score,
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
            
			# Generate signal (informational; not scored in confluence)
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
				"score": 0,
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
    
	# ===============
	# PAPA + SMM Core
	# ===============

	def _find_swings(self, series: pd.Series, window: int = 3, kind: str = 'high') -> List[pd.Timestamp]:
		idxs = []
		for i in range(window, len(series) - window):
			window_slice = series.iloc[i - window:i + window + 1]
			center = series.iloc[i]
			if kind == 'high':
				if center == window_slice.max() and (window_slice == center).sum() == 1:
					idxs.append(series.index[i])
			else:
				if center == window_slice.min() and (window_slice == center).sum() == 1:
					idxs.append(series.index[i])
		return idxs

	def analyze_primary_trend(self) -> Dict[str, Union[str, Dict, List]]:
		try:
			if self.data is None:
				self._fetch_data()
			highs = self._find_swings(self.data['High'], window=3, kind='high')
			lows = self._find_swings(self.data['Low'], window=3, kind='low')

			last_highs = highs[-3:]
			last_lows = lows[-3:]

			trend = 'Sideways'
			reason = 'Insufficient swing points'
			if len(last_highs) >= 2 and len(last_lows) >= 2:
				h_vals = [self.data.loc[i, 'High'] for i in last_highs[-2:]]
				l_vals = [self.data.loc_iat[self.data.index.get_loc(last_lows[-2]), self.data.columns.get_loc('Low')],
						  self.data.loc_iat[self.data.index.get_loc(last_lows[-1]), self.data.columns.get_loc('Low')]] if False else [self.data.loc[last_lows[-2], 'Low'], self.data.loc[last_lows[-1], 'Low']]
				if h_vals[1] > h_vals[0] and l_vals[1] > l_vals[0]:
					trend = 'Uptrend'
					reason = 'Higher Highs and Higher Lows'
				elif h_vals[1] < h_vals[0] and l_vals[1] < l_vals[0]:
					trend = 'Downtrend'
					reason = 'Lower Highs and Lower Lows'
				else:
					trend = 'Sideways'
					reason = 'Mixed swing structure'

			return {
				'trend': trend,
				'reason': reason,
				'swings': {
					'highs': [{ 'date': str(ts), 'price': float(self.data.loc[ts, 'High']) } for ts in last_highs],
					'lows': [{ 'date': str(ts), 'price': float(self.data.loc[ts, 'Low']) } for ts in last_lows],
				}
			}
		except Exception as e:
			return { 'trend': 'Sideways', 'reason': f'Error in primary trend: {e}', 'error': True }

	def analyze_candlestick_patterns(self) -> Dict[str, Union[str, int, Dict, List]]:
		try:
			if self.data is None:
				self._fetch_data()
			if len(self.data) < 3:
				return { 'signal': 'HOLD', 'score': 0, 'details': 'Insufficient candles' }

			trend_info = self.analyze_primary_trend()
			trend = trend_info.get('trend', 'Sideways')
			o = self.data['Open']
			h = self.data['High']
			l = self.data['Low']
			c = self.data['Close']
			patterns = []
			score = 0

			# Helper recent move
			last3 = c.tail(3).values
			up_move = last3[2] > last3[1] > last3[0]
			down_move = last3[2] < last3[1] < last3[0]

			# Engulfing
			prev = -2
			curr = -1
			bullish_engulf = (c.iloc[curr] > o.iloc[curr]) and (c.iloc[prev] < o.iloc[prev]) and (c.iloc[curr] >= o.iloc[prev]) and (o.iloc[curr] <= c.iloc[prev])
			bearish_engulf = (c.iloc[curr] < o.iloc[curr]) and (c.iloc[prev] > o.iloc[prev]) and (c.iloc[curr] <= o.iloc[prev]) and (o.iloc[curr] >= c.iloc[prev])
			if bullish_engulf:
				if trend != 'Downtrend':
					score += 2
				patterns.append('Bullish Engulfing')
			if bearish_engulf:
				if trend != 'Uptrend':
					score -= 2
				patterns.append('Bearish Engulfing')

			# Hammer / Shooting Star
			body = abs(c.iloc[curr] - o.iloc[curr])
			upper = h.iloc[curr] - max(c.iloc[curr], o.iloc[curr])
			lower = min(c.iloc[curr], o.iloc[curr]) - l.iloc[curr]
			if lower >= 2 * body and upper <= body and down_move:
				score += 1
				patterns.append('Hammer')
			if upper >= 2 * body and lower <= body and up_move:
				score -= 1
				patterns.append('Shooting Star')

			# Morning/Evening Star (approx, no strict gaps)
			b1_body = abs(c.iloc[-3] - o.iloc[-3])
			b2_body = abs(c.iloc[-2] - o.iloc[-2])
			b3_body = abs(c.iloc[-1] - o.iloc[-1])
			is_bear1 = c.iloc[-3] < o.iloc[-3]
			is_bull3 = c.iloc[-1] > o.iloc[-1]
			is_bull1 = c.iloc[-3] > o.iloc[-3]
			is_bear3 = c.iloc[-1] < o.iloc[-1]
			# Morning Star
			if is_bear1 and b2_body < b1_body * 0.6 and is_bull3 and c.iloc[-1] > (o.iloc[-3] + c.iloc[-3]) / 2:
				score += 2
				patterns.append('Morning Star')
			# Evening Star
			if is_bull1 and b2_body < b1_body * 0.6 and is_bear3 and c.iloc[-1] < (o.iloc[-3] + c.iloc[-3]) / 2:
				score -= 2
				patterns.append('Evening Star')

			signal = 'BUY' if score > 0 else 'SELL' if score < 0 else 'HOLD'
			return {
				'signal': signal,
				'score': int(score),
				'details': f"Patterns: {', '.join(patterns) if patterns else 'None'} (trend: {trend})",
				'patterns': patterns,
				'trend_context': trend
			}
		except Exception as e:
			return { 'signal': 'HOLD', 'score': 0, 'details': f'Error in candlestick patterns: {e}', 'error': True }

	def analyze_chart_patterns(self) -> Dict[str, Union[str, int, Dict]]:
		try:
			if self.data is None:
				self._fetch_data()
			lookback = 20
			high = self.data['High']
			low = self.data['Low']
			vol = self.data['Volume'] if 'Volume' in self.data.columns else pd.Series(index=self.data.index, data=np.nan)
			avg_vol = vol.rolling(20).mean().iloc[-1] if vol.notna().any() else np.nan

			last_idx = self.data.index[-1]
			mother_idx = None
			mother_high = mother_low = None
			# Find latest mother candle with at least 1 inside bar following
			for i in range(len(self.data) - 2, len(self.data) - lookback - 1, -1):
				if i < 1:
					break
				h_i, l_i = high.iloc[i], low.iloc[i]
				h_next, l_next = high.iloc[i + 1], low.iloc[i + 1]
				if h_next < h_i and l_next > l_i:
					mother_idx = self.data.index[i]
					mother_high = h_i
					mother_low = l_i
					break

			if mother_idx is None:
				return { 'signal': 'HOLD', 'score': 0, 'details': 'No recent Mother Candle with inside bar', 'pattern': None }

			last_high = high.iloc[-1]
			last_low = low.iloc[-1]
			last_close = self.data['Close'].iloc[-1]
			last_vol = vol.iloc[-1] if vol.notna().any() else np.nan
			has_breakout_up = last_high > mother_high or last_close > mother_high
			has_breakdown = last_low < mother_low or last_close < mother_low
			vol_ok = (not np.isnan(avg_vol)) and (not np.isnan(last_vol)) and (last_vol > avg_vol)

			score = 0
			details = f"Mother@{mother_idx.date()} range [{mother_low:.2f}, {mother_high:.2f}]"
			signal = 'HOLD'
			if has_breakout_up and vol_ok:
				score = +2
				signal = 'BUY'
				details += ' | Bullish breakout with above-average volume'
			elif has_breakdown and vol_ok:
				score = -2
				signal = 'SELL'
				details += ' | Bearish breakdown with above-average volume'
			else:
				details += ' | No confirmed break with volume'

			return {
				'signal': signal,
				'score': score,
				'details': details,
				'pattern': {
					'mother_index': str(mother_idx),
					'mother_high': float(mother_high),
					'mother_low': float(mother_low)
				}
			}
		except Exception as e:
			return { 'signal': 'HOLD', 'score': 0, 'details': f'Error in chart patterns: {e}', 'error': True }

	def analyze_divergence(self, lookback: int = 40, rsi_window: int = 14) -> Dict[str, Union[str, int, Dict]]:
		try:
			if self.data is None:
				self._fetch_data()
			close = self.data['Close']
			# RSI
			delta = close.diff()
			gain = (delta.where(delta > 0, 0)).rolling(window=rsi_window).mean()
			loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_window).mean()
			rs = gain / loss
			rsi = 100 - (100 / (1 + rs))

			price_lows_idx = self._find_swings(close.tail(lookback+20), window=3, kind='low')
			price_highs_idx = self._find_swings(close.tail(lookback+20), window=3, kind='high')
			# Ensure we only keep last two
			p_lows = price_lows_idx[-2:]
			p_highs = price_highs_idx[-2:]
			score = 0
			signal = 'HOLD'
			details = 'No clear divergence'
			if len(p_lows) == 2:
				p1, p2 = p_lows[0], p_lows[1]
				if close.loc[p2] < close.loc[p1] and rsi.loc[p2] > rsi.loc[p1]:
					score = +3
					signal = 'BUY'
					details = 'Bullish divergence: lower low in price, higher low in RSI'
			if len(p_highs) == 2:
				p1, p2 = p_highs[0], p_highs[1]
				if close.loc[p2] > close.loc[p1] and rsi.loc[p2] < rsi.loc[p1]:
					score = -3
					signal = 'SELL'
					details = 'Bearish divergence: higher high in price, lower high in RSI'

			return {
				'signal': signal,
				'score': score,
				'details': details
			}
		except Exception as e:
			return { 'signal': 'HOLD', 'score': 0, 'details': f'Error in divergence: {e}', 'error': True }


