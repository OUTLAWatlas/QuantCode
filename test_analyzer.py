"""
QUANTCODE Test Suite
===================

Test and demonstration script for the Heiken Ashi trading analysis function.
"""

from backend.quantcode_analyzer import analyze_heiken_ashi
import warnings

# Suppress pandas warnings for cleaner output
warnings.filterwarnings('ignore')

def test_single_ticker(ticker):
    """Test analysis for a single ticker and display results."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {ticker}")
    print('='*60)
    
    try:
        result = analyze_heiken_ashi(ticker)
        
        print(f"✅ SUCCESS")
        print(f"   Ticker: {result['ticker']}")
        print(f"   Signal: {result['signal']}")
        print(f"   Strategy: {result['strategy']}")
        print(f"   Latest Close Price: ${result['latest_close_price']:.2f}")
        
        # Explain the signal
        if result['signal'] == 'BUY':
            print(f"   📈 BUY Signal: Bullish candle with no lower wick (decisive)")
        elif result['signal'] == 'SELL':
            print(f"   📉 SELL Signal: Bearish candle with no upper wick (decisive)")
        else:
            print(f"   ⏸️  HOLD Signal: Conditions not met for decisive action")
            
        return result
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def test_error_handling():
    """Test error handling with invalid inputs."""
    print(f"\n{'='*60}")
    print("Testing Error Handling")
    print('='*60)
    
    test_cases = [
        ("", "Empty ticker"),
        ("INVALID123", "Invalid ticker"),
        (None, "None input"),
        (123, "Non-string input")
    ]
    
    for ticker, description in test_cases:
        print(f"\nTesting {description}:")
        try:
            result = analyze_heiken_ashi(ticker)
            print(f"  Unexpected success: {result}")
        except Exception as e:
            print(f"  ✅ Expected error: {type(e).__name__}: {e}")

def main():
    """Main test function."""
    print("QUANTCODE - Heiken Ashi Trading Analysis")
    print("=" * 60)
    print("Testing the analyze_heiken_ashi function")
    
    # Test with various stock tickers
    test_tickers = [
        "AAPL",          # Apple
        "TSLA",          # Tesla
        "MSFT",          # Microsoft
        "RELIANCE.NS",   # Reliance (Indian stock)
        "TCS.NS",        # TCS (Indian stock)
    ]
    
    results = []
    for ticker in test_tickers:
        result = test_single_ticker(ticker)
        if result:
            results.append(result)
    
    # Test error handling
    test_error_handling()
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"Successfully analyzed {len(results)} tickers:")
    
    for result in results:
        signal_emoji = "📈" if result['signal'] == 'BUY' else "📉" if result['signal'] == 'SELL' else "⏸️"
        print(f"  {signal_emoji} {result['ticker']}: {result['signal']} (${result['latest_close_price']:.2f})")

if __name__ == "__main__":
    main()