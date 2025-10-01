"""
Flask API for QuantCode Trading Analysis
========================================

A RESTful API that provides comprehensive trading analysis using multiple
technical indicators through the QuantCodeAnalyzer class.

Author: QuantCode Team
Date: October 2025
"""

from flask import Flask, jsonify, request
from quantcode_analyzer import QuantCodeAnalyzer
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)


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
            "/api/calculate_position_size": "GET - Calculate position size for risk management",
            "/health": "GET - API health check"
        },
        "examples": {
            "analysis": "/analyze/AAPL",
            "position_size": "/api/calculate_position_size?account=10000&risk=1&entry=100&sl=95"
        }
    })

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
        days (int): Number of days of historical data (default: 100)
        
    Returns:
        JSON response with complete analysis
    """
    try:
        # Get optional parameters
        days = request.args.get('days', 100, type=int)
        
        # Validate days parameter
        if days < 20 or days > 365:
            return jsonify({
                "error": "Invalid days parameter. Must be between 20 and 365.",
                "ticker": ticker
            }), 400
        
        # Initialize analyzer and get results
        analyzer = QuantCodeAnalyzer(ticker.upper(), days=days)
        result = analyzer.get_final_signal()
        
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
        days = request.args.get('days', 100, type=int)
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
        days = request.args.get('days', 100, type=int)
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
        days = request.args.get('days', 100, type=int)
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
        days = request.args.get('days', 100, type=int)
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
        days = data.get('days', 100)
        
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