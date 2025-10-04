"""
Flask API for QuantCode Trading Analysis
========================================

A RESTful API that provides comprehensive trading analysis using multiple
technical indicators through the QuantCodeAnalyzer class.

Author: QuantCode Team
Date: October 2025
"""

from flask import Flask, jsonify, request
from backend.quantcode_analyzer import QuantCodeAnalyzer
import logging
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from typing import Any, Dict, Tuple
import os
from models import db, Ticker, AnalysisResult
from flask_migrate import Migrate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# --------------------
# Database configuration
# --------------------
default_sqlite_uri = 'sqlite:///quantcode.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', default_sqlite_uri)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)
Migrate(app, db)

# Auto-initialize SQLite schema for local development when using the fallback DB
try:
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if uri.startswith('sqlite'):
        with app.app_context():
            from sqlalchemy import inspect
            insp = inspect(db.engine)
            needed_tables = ['tickers', 'analysis_results', 'paper_trades']
            missing = [t for t in needed_tables if not insp.has_table(t)]
            if missing:
                db.create_all()
                logger.info(f"Initialized SQLite DB with tables: {', '.join(needed_tables)}")
except Exception as e:
    logger.warning(f"SQLite bootstrap failed: {e}")

# -----------------------
# Simple in-memory caches
# -----------------------
# Note: Suitable for a single-process dev server. For production, prefer Redis/memcached.

AnalyzeCache: Dict[Tuple[str, int], Dict[str, Any]] = {}
AnalyzeCacheMeta: Dict[Tuple[str, int], float] = {}
AnalyzeCacheTTL = 180  # seconds
AnalyzeCacheMaxKeys = 200

HistoryCache: Dict[Tuple[str, int], Dict[str, Any]] = {}
HistoryCacheMeta: Dict[Tuple[str, int], float] = {}
HistoryCacheTTL = 600  # seconds
HistoryCacheMaxKeys = 300

def _cache_get(cache: Dict, meta: Dict, key: Tuple, ttl: int):
    now = datetime.now().timestamp()
    ts = meta.get(key)
    if ts is None:
        return None
    if now - ts > ttl:
        # expired
        cache.pop(key, None)
        meta.pop(key, None)
        return None
    return cache.get(key)

def _cache_set(cache: Dict, meta: Dict, key: Tuple, value: Any, max_keys: int):
    # Evict oldest if exceeding max
    if len(cache) >= max_keys:
        # find oldest by timestamp
        oldest_key = None
        oldest_ts = float('inf')
        for k, ts in meta.items():
            if ts < oldest_ts:
                oldest_ts = ts
                oldest_key = k
        if oldest_key is not None:
            cache.pop(oldest_key, None)
            meta.pop(oldest_key, None)
    cache[key] = value
    meta[key] = datetime.now().timestamp()


def calculate_position_size(account_value, risk_percent, stop_loss_price, entry_price):
    """
    Calculate the maximum position size based on the 1% risk management rule.
    
    This function implements the fractional risk model where traders risk a fixed
    percentage of their account value on each trade. The position size is calculated
    to ensure that if the stop loss is hit, the loss will be exactly the specified
    percentage of the account value.
    
    Args:
        account_value (float): Total account value in dollars
        risk_percent (float): Percentage of account to risk per trade (e.g., 1.0 for 1%)
        stop_loss_price (float): Stop loss price per share
        entry_price (float): Entry price per share
    
    Returns:
        dict: Dictionary containing calculated values:
            - max_shares: Maximum number of shares to trade
            - risk_amount: Dollar amount being risked
            - risk_per_share: Risk per share in dollars
            - account_value: Input account value
            - risk_percent: Input risk percentage
            - entry_price: Input entry price
            - stop_loss_price: Input stop loss price
    
    Example:
        >>> calculate_position_size(10000, 1.0, 95.0, 100.0)
        {
            'max_shares': 20,
            'risk_amount': 100.0,
            'risk_per_share': 5.0,
            'account_value': 10000,
            'risk_percent': 1.0,
            'entry_price': 100.0,
            'stop_loss_price': 95.0
        }
    """
    try:
        # Calculate the dollar amount to risk per trade
        risk_amount_per_trade = account_value * (risk_percent / 100.0)
        
        # Calculate the risk per share (difference between entry and stop loss)
        risk_per_share = abs(entry_price - stop_loss_price)
        
        # Handle division by zero case
        if risk_per_share == 0:
            return {
                'max_shares': 0,
                'risk_amount': risk_amount_per_trade,
                'risk_per_share': 0,
                'account_value': account_value,
                'risk_percent': risk_percent,
                'entry_price': entry_price,
                'stop_loss_price': stop_loss_price,
                'error': 'Entry price and stop loss price cannot be the same'
            }
        
        # Calculate maximum shares that can be traded
        max_shares = int(risk_amount_per_trade / risk_per_share)
        
        return {
            'max_shares': max_shares,
            'risk_amount': round(risk_amount_per_trade, 2),
            'risk_per_share': round(risk_per_share, 2),
            'account_value': account_value,
            'risk_percent': risk_percent,
            'entry_price': entry_price,
            'stop_loss_price': stop_loss_price
        }
        
    except Exception as e:
        return {
            'max_shares': 0,
            'risk_amount': 0,
            'risk_per_share': 0,
            'account_value': account_value,
            'risk_percent': risk_percent,
            'entry_price': entry_price,
            'stop_loss_price': stop_loss_price,
            'error': f'Calculation error: {str(e)}'
        }

@app.route('/')
def home():
    """API home endpoint with usage information."""
    return jsonify({
        "message": "QuantCode Trading Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "/analyze/<ticker>": "GET - Comprehensive analysis for a ticker",
            "/analyze/<ticker>/heiken-ashi": "GET - Heiken Ashi analysis only",
            "/analyze/<ticker>/bollinger": "GET - Bollinger Bands analysis only",
            "/analyze/<ticker>/macd": "GET - MACD analysis only",
            "/analyze/<ticker>/rsi": "GET - RSI analysis only",
            "/api/tickers": "GET - List watched tickers | POST - Replace watched tickers",
            "/api/history/<ticker>": "GET - Historical close series for charts (time,value)",
            "/api/calculate_position_size": "GET - Calculate position size for risk management",
            "/health": "GET - API health check"
        },
        "examples": {
            "analysis": "/analyze/AAPL",
            "position_size": "/api/calculate_position_size?account=10000&risk=1&entry=100&sl=95",
            "history": "/api/history/AAPL?days=200"
        }
    })

@app.route('/api/tickers', methods=['GET'])
def get_watched_tickers():
    """Return list of watched ticker symbols from the database.

    Response: ["AAPL", "GOOG", ...]
    """
    try:
        # Prefer Flask-SQLAlchemy style query if available
        rows = Ticker.query.all() if hasattr(Ticker, 'query') else db.session.query(Ticker).all()
        symbols = []
        for r in rows:
            sym = getattr(r, 'symbol', None) or getattr(r, 'ticker', None)
            if sym is None:
                # Fallback to string representation
                sym = str(r)
            symbols.append(str(sym))
        return jsonify(symbols)
    except Exception as e:
        logger.error(f"/api/tickers GET failed: {e}")
        return jsonify({ 'error': 'Failed to fetch tickers', 'details': str(e) }), 500

@app.route('/api/tickers', methods=['POST'])
def replace_watched_tickers():
    """Replace all watched tickers with the provided list.

    Request JSON: { "tickers": ["AAPL", "GOOG"] }
    Response JSON: { "status": "success", "count": 2 }
    """
    try:
        payload = request.get_json(silent=True) or {}
        tickers = payload.get('tickers')
        if not isinstance(tickers, list):
            return jsonify({ 'error': "Body must include 'tickers' as a list" }), 400
        # Normalize and filter
        new_syms = [str(s).strip().upper() for s in tickers if isinstance(s, (str, bytes)) and str(s).strip()]

        # Determine model attribute to set
        field_name = 'symbol' if hasattr(Ticker, 'symbol') else ('ticker' if hasattr(Ticker, 'ticker') else None)
        if field_name is None:
            return jsonify({ 'error': 'Ticker model missing symbol/ticker attribute' }), 500

        # Replace all entries atomically
        try:
            # Delete all existing entries
            if hasattr(Ticker, 'query'):
                Ticker.query.delete()
            else:
                db.session.query(Ticker).delete()
            # Insert new
            for sym in new_syms:
                db.session.add(Ticker(**{field_name: sym}))
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return jsonify({ 'status': 'success', 'count': len(new_syms) })
    except Exception as e:
        logger.error(f"/api/tickers POST failed: {e}")
        return jsonify({ 'error': 'Failed to replace tickers', 'details': str(e) }), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "api": "QuantCode Trading Analysis",
        "version": "1.0.0"
    })

@app.route('/analyze/<ticker>')
def analyze_ticker(ticker):
    """
    Comprehensive analysis endpoint that returns all indicators and final signal.
    
    Args:
        ticker (str): Stock ticker symbol
        
    Query Parameters:
        days (int): Number of days of historical data (default: 200)
        
    Returns:
        JSON response with complete analysis
    """
    try:
        # Get optional parameters
        days = request.args.get('days', 200, type=int)
        
        # Validate days parameter
        if days < 20 or days > 365:
            return jsonify({
                "error": "Invalid days parameter. Must be between 20 and 365.",
                "ticker": ticker
            }), 400
        
        # Cache key and nocache override
        key = (ticker.upper(), int(days))
        nocache = request.args.get('nocache', '0') in ('1', 'true', 'True')

        if not nocache:
            cached = _cache_get(AnalyzeCache, AnalyzeCacheMeta, key, AnalyzeCacheTTL)
            if cached is not None:
                logger.info(f"Analyze cache hit for {ticker}:{days}")
                return jsonify(cached)

        # Initialize analyzer and get results
        analyzer = QuantCodeAnalyzer(ticker.upper(), days=days)
        result = analyzer.get_final_signal()

        # Persist analysis result if successful (no error key)
        try:
            if not result.get('error'):
                # Extract primary trend text
                pt = result.get('primary_trend')
                primary_trend_text = pt.get('trend') if isinstance(pt, dict) else (pt or None)
                ar = AnalysisResult(
                    ticker_symbol=ticker.upper(),
                    final_signal=result.get('final_signal'),
                    total_score=int(result.get('total_score', 0)),
                    primary_trend=primary_trend_text,
                    breakdown=result.get('analyses', {})
                )
                db.session.add(ar)
                db.session.commit()
        except Exception as e:
            # Do not fail the API for persistence errors; just log and continue
            try:
                db.session.rollback()
            except Exception:
                pass
            logger.error(f"Failed to persist analysis result for {ticker}: {e}")

        # Store in cache
        _cache_set(AnalyzeCache, AnalyzeCacheMeta, key, result, AnalyzeCacheMaxKeys)
        
        # Log the analysis
        logger.info(f"Analysis completed for {ticker}: {result['final_signal']}")
        
        return jsonify(result)
        
    except ValueError as ve:
        logger.warning(f"Validation error for {ticker}: {str(ve)}")
        return jsonify({
            "error": str(ve),
            "ticker": ticker,
            "type": "validation_error"
        }), 400
        
    except Exception as e:
        logger.error(f"Server error for {ticker}: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "ticker": ticker,
            "type": "server_error",
            "details": str(e)
        }), 500

@app.route('/analyze/<ticker>/heiken-ashi')
def analyze_heiken_ashi_only(ticker):
    """Heiken Ashi analysis only endpoint."""
    try:
        days = request.args.get('days', 200, type=int)
        analyzer = QuantCodeAnalyzer(ticker.upper(), days=days)
        result = analyzer.analyze_heiken_ashi()
        
        return jsonify({
            "ticker": ticker.upper(),
            "analysis_type": "heiken_ashi",
            "latest_close_price": analyzer.latest_close_price,
            "result": result
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "ticker": ticker,
            "analysis_type": "heiken_ashi"
        }), 500

@app.route('/analyze/<ticker>/bollinger')
def analyze_bollinger_only(ticker):
    """Bollinger Bands analysis only endpoint."""
    try:
        days = request.args.get('days', 200, type=int)
        window = request.args.get('window', 20, type=int)
        std_dev = request.args.get('std_dev', 2, type=int)
        
        analyzer = QuantCodeAnalyzer(ticker.upper(), days=days)
        result = analyzer.analyze_bollinger_bands(window=window, std_dev=std_dev)
        
        return jsonify({
            "ticker": ticker.upper(),
            "analysis_type": "bollinger_bands",
            "parameters": {"window": window, "std_dev": std_dev},
            "latest_close_price": analyzer.latest_close_price,
            "result": result
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "ticker": ticker,
            "analysis_type": "bollinger_bands"
        }), 500

@app.route('/analyze/<ticker>/macd')
def analyze_macd_only(ticker):
    """MACD analysis only endpoint."""
    try:
        days = request.args.get('days', 200, type=int)
        fast = request.args.get('fast', 12, type=int)
        slow = request.args.get('slow', 26, type=int)
        signal = request.args.get('signal', 9, type=int)
        
        analyzer = QuantCodeAnalyzer(ticker.upper(), days=days)
        result = analyzer.analyze_macd(fast=fast, slow=slow, signal=signal)
        
        return jsonify({
            "ticker": ticker.upper(),
            "analysis_type": "macd",
            "parameters": {"fast": fast, "slow": slow, "signal": signal},
            "latest_close_price": analyzer.latest_close_price,
            "result": result
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "ticker": ticker,
            "analysis_type": "macd"
        }), 500

@app.route('/analyze/<ticker>/rsi')
def analyze_rsi_only(ticker):
    """RSI analysis only endpoint."""
    try:
        days = request.args.get('days', 200, type=int)
        window = request.args.get('window', 14, type=int)
        
        analyzer = QuantCodeAnalyzer(ticker.upper(), days=days)
        result = analyzer.analyze_rsi(window=window)
        
        return jsonify({
            "ticker": ticker.upper(),
            "analysis_type": "rsi",
            "parameters": {"window": window},
            "latest_close_price": analyzer.latest_close_price,
            "result": result
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "ticker": ticker,
            "analysis_type": "rsi"
        }), 500

@app.route('/batch-analyze', methods=['POST'])
def batch_analyze():
    """
    Batch analysis endpoint for multiple tickers.
    
    Expected JSON payload:
    {
        "tickers": ["AAPL", "TSLA", "MSFT"],
        "days": 100  // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'tickers' not in data:
            return jsonify({
                "error": "Missing 'tickers' field in request body"
            }), 400
        
        tickers = data['tickers']
        days = data.get('days', 200)
        
        if not isinstance(tickers, list) or len(tickers) == 0:
            return jsonify({
                "error": "Tickers must be a non-empty list"
            }), 400
        
        if len(tickers) > 10:  # Limit batch size
            return jsonify({
                "error": "Maximum 10 tickers allowed per batch request"
            }), 400
        
        results = []
        errors = []
        
        for ticker in tickers:
            try:
                analyzer = QuantCodeAnalyzer(ticker.upper(), days=days)
                result = analyzer.get_final_signal()
                results.append(result)
            except Exception as e:
                errors.append({
                    "ticker": ticker,
                    "error": str(e)
                })
        
        return jsonify({
            "batch_results": results,
            "errors": errors,
            "summary": {
                "total_requested": len(tickers),
                "successful": len(results),
                "failed": len(errors)
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": "Invalid request format",
            "details": str(e)
        }), 400

@app.route('/api/calculate_position_size', methods=['GET'])
def calculate_position_size_endpoint():
    """
    Calculate position size based on risk management rules.
    
    Query Parameters:
        account (float): Total account value in dollars
        risk (float): Risk percentage per trade (e.g., 1.0 for 1%)
        entry (float): Entry price per share
        sl (float): Stop loss price per share
    
    Returns:
        JSON response with calculated position size and risk metrics
    
    Example:
        GET /api/calculate_position_size?account=10000&risk=1&entry=100&sl=95
    """
    try:
        # Extract query parameters
        account_value = request.args.get('account', type=float)
        risk_percent = request.args.get('risk', type=float)
        entry_price = request.args.get('entry', type=float)
        stop_loss_price = request.args.get('sl', type=float)
        
        # Validate required parameters
        if account_value is None:
            return jsonify({
                "error": "Missing required parameter: account",
                "message": "Please provide account value as 'account' parameter"
            }), 400
            
        if risk_percent is None:
            return jsonify({
                "error": "Missing required parameter: risk",
                "message": "Please provide risk percentage as 'risk' parameter"
            }), 400
            
        if entry_price is None:
            return jsonify({
                "error": "Missing required parameter: entry",
                "message": "Please provide entry price as 'entry' parameter"
            }), 400
            
        if stop_loss_price is None:
            return jsonify({
                "error": "Missing required parameter: sl",
                "message": "Please provide stop loss price as 'sl' parameter"
            }), 400
        
        # Validate parameter values
        if account_value <= 0:
            return jsonify({
                "error": "Invalid account value",
                "message": "Account value must be greater than 0"
            }), 400
            
        if risk_percent <= 0 or risk_percent > 100:
            return jsonify({
                "error": "Invalid risk percentage",
                "message": "Risk percentage must be between 0.01 and 100"
            }), 400
            
        if entry_price <= 0:
            return jsonify({
                "error": "Invalid entry price",
                "message": "Entry price must be greater than 0"
            }), 400
            
        if stop_loss_price <= 0:
            return jsonify({
                "error": "Invalid stop loss price",
                "message": "Stop loss price must be greater than 0"
            }), 400
        
        # Calculate position size
        result = calculate_position_size(account_value, risk_percent, stop_loss_price, entry_price)
        
        # Log the calculation for monitoring
        logger.info(f"Position size calculated: Account=${account_value}, Risk={risk_percent}%, "
                   f"Entry=${entry_price}, SL=${stop_loss_price}, Shares={result['max_shares']}")
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "calculation": result,
            "recommendation": {
                "max_shares": result['max_shares'],
                "total_investment": round(result['max_shares'] * entry_price, 2),
                "max_loss_if_sl_hit": result['risk_amount'],
                "risk_to_reward_setup": "1% account risk per trade"
            }
        })
        
    except Exception as e:
        logger.error(f"Error in position size calculation: {str(e)}")
        return jsonify({
            "error": "Calculation failed",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/history/<ticker>', methods=['GET'])
def get_history_series(ticker: str):
    """Provide historical close price series for charts.

    Query params:
        days: int (default 200) — number of calendar days to fetch.

    Returns: { series: [{ time: 'YYYY-MM-DD', value: float }, ...] }
    """
    try:
        days = request.args.get('days', 200, type=int)
        if days < 20 or days > 730:
            return jsonify({
                'error': 'Invalid days parameter. Must be between 20 and 730.'
            }), 400

        # Cache key and nocache override
        key = (ticker.upper(), int(days))
        nocache = request.args.get('nocache', '0') in ('1', 'true', 'True')

        if not nocache:
            cached = _cache_get(HistoryCache, HistoryCacheMeta, key, HistoryCacheTTL)
            if cached is not None:
                logger.info(f"History cache hit for {ticker}:{days}")
                return jsonify(cached)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=True,
            prepost=True,
            group_by='column'
        )
        if df.empty:
            return jsonify({ 'series': [] })

        # Ensure datetime index for consistent formatting
        try:
            df.index = pd.to_datetime(df.index)
        except Exception:
            pass

        def _to_date_str(idx_val):
            try:
                # pandas Timestamp or datetime
                return idx_val.strftime('%Y-%m-%d')
            except Exception:
                s = str(idx_val)
                # Fallback: try first 10 chars if looks like date
                return s[:10]

        # Flatten columns if MultiIndex and extract a 1D Close series
        if isinstance(df.columns, pd.MultiIndex):
            try:
                df.columns = df.columns.droplevel(1)
            except Exception:
                pass

        close_series = None
        if 'Close' in df.columns:
            close_obj = df['Close']
            # Ensure it's a Series
            close_series = close_obj.iloc[:, 0] if hasattr(close_obj, 'columns') else close_obj
        elif 'Adj Close' in df.columns:
            close_obj = df['Adj Close']
            close_series = close_obj.iloc[:, 0] if hasattr(close_obj, 'columns') else close_obj
        else:
            raise ValueError("Close prices not found in downloaded data")

        series = [{ 'time': _to_date_str(idx), 'value': float(val) } for idx, val in close_series.dropna().items()]
        payload = { 'series': series, 'ticker': ticker.upper() }
        _cache_set(HistoryCache, HistoryCacheMeta, key, payload, HistoryCacheMaxKeys)
        return jsonify(payload)
    except Exception as e:
        logger.error(f"History endpoint error for {ticker}: {e}")
        return jsonify({ 'error': 'Failed to fetch history', 'details': str(e) }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Endpoint not found",
        "message": "Please check the API documentation at the root endpoint"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "error": "Internal server error",
        "message": "Please try again later"
    }), 500

if __name__ == '__main__':
    # Run the Flask development server
    print("🚀 Starting QuantCode Trading Analysis API...")
    print("📊 Access the API at: http://localhost:5000")
    print("📖 API Documentation: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)