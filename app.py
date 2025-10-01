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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

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
            "/health": "GET - API health check"
        },
        "example": "/analyze/AAPL"
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