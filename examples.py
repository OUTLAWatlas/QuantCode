"""
QUANTCODE Usage Examples
=======================

Practical examples demonstrating how to use the analyze_heiken_ashi function
in different trading scenarios and applications.
"""

from quantcode_analyzer import analyze_heiken_ashi
import json
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def example_single_analysis():
    """Example 1: Analyze a single stock."""
    print("Example 1: Single Stock Analysis")
    print("-" * 40)
    
    ticker = "AAPL"
    result = analyze_heiken_ashi(ticker)
    
    print(f"Analyzing {ticker}:")
    print(f"Signal: {result['signal']}")
    print(f"Close Price: ${result['latest_close_price']:.2f}")
    print(f"Strategy: {result['strategy']}")
    print()

def example_portfolio_screening():
    """Example 2: Screen a portfolio of stocks."""
    print("Example 2: Portfolio Screening")
    print("-" * 40)
    
    portfolio = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN"]
    
    buy_signals = []
    sell_signals = []
    hold_signals = []
    
    for ticker in portfolio:
        try:
            result = analyze_heiken_ashi(ticker)
            
            if result['signal'] == 'BUY':
                buy_signals.append(result)
            elif result['signal'] == 'SELL':
                sell_signals.append(result)
            else:
                hold_signals.append(result)
                
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
    
    print(f"📈 BUY Signals ({len(buy_signals)}):")
    for signal in buy_signals:
        print(f"  • {signal['ticker']}: ${signal['latest_close_price']:.2f}")
    
    print(f"📉 SELL Signals ({len(sell_signals)}):")
    for signal in sell_signals:
        print(f"  • {signal['ticker']}: ${signal['latest_close_price']:.2f}")
    
    print(f"⏸️  HOLD Signals ({len(hold_signals)}):")
    for signal in hold_signals:
        print(f"  • {signal['ticker']}: ${signal['latest_close_price']:.2f}")
    print()

def example_indian_stocks():
    """Example 3: Analyze Indian market stocks."""
    print("Example 3: Indian Market Analysis")
    print("-" * 40)
    
    indian_stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFC.NS", "ICICIBANK.NS"]
    
    results = []
    for ticker in indian_stocks:
        try:
            result = analyze_heiken_ashi(ticker)
            results.append(result)
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
    
    # Sort by signal priority (BUY > SELL > HOLD)
    signal_priority = {'BUY': 1, 'SELL': 2, 'HOLD': 3}
    results.sort(key=lambda x: signal_priority[x['signal']])
    
    print("Indian Stock Analysis Results:")
    for result in results:
        emoji = "📈" if result['signal'] == 'BUY' else "📉" if result['signal'] == 'SELL' else "⏸️"
        print(f"  {emoji} {result['ticker']}: {result['signal']} (₹{result['latest_close_price']:.2f})")
    print()

def example_json_output():
    """Example 4: Generate JSON output for API integration."""
    print("Example 4: JSON Output for API Integration")
    print("-" * 40)
    
    tickers = ["AAPL", "TSLA"]
    results = []
    
    for ticker in tickers:
        try:
            result = analyze_heiken_ashi(ticker)
            results.append(result)
        except Exception as e:
            results.append({
                "ticker": ticker,
                "error": str(e),
                "signal": None,
                "strategy": None,
                "latest_close_price": None
            })
    
    # Convert to JSON
    json_output = json.dumps(results, indent=2)
    print("JSON Output:")
    print(json_output)
    print()

def example_trading_alert():
    """Example 5: Simple trading alert system."""
    print("Example 5: Trading Alert System")
    print("-" * 40)
    
    watchlist = ["AAPL", "TSLA", "RELIANCE.NS", "TCS.NS"]
    
    alerts = []
    
    for ticker in watchlist:
        try:
            result = analyze_heiken_ashi(ticker)
            
            if result['signal'] in ['BUY', 'SELL']:
                alerts.append({
                    'ticker': result['ticker'],
                    'action': result['signal'],
                    'price': result['latest_close_price'],
                    'timestamp': '2025-10-01 Current Time'  # In real app, use actual timestamp
                })
        except Exception as e:
            print(f"Alert system error for {ticker}: {e}")
    
    if alerts:
        print("🚨 TRADING ALERTS:")
        for alert in alerts:
            action_emoji = "📈" if alert['action'] == 'BUY' else "📉"
            print(f"  {action_emoji} {alert['action']} {alert['ticker']} at ${alert['price']:.2f}")
            print(f"     Time: {alert['timestamp']}")
    else:
        print("✅ No trading alerts at this time.")
    print()

def main():
    """Run all examples."""
    print("QUANTCODE - Usage Examples")
    print("=" * 50)
    print()
    
    example_single_analysis()
    example_portfolio_screening()
    example_indian_stocks()
    example_json_output()
    example_trading_alert()
    
    print("=" * 50)
    print("All examples completed!")
    print("\nNote: This is a demonstration using live market data.")
    print("Signals are for educational purposes only and should not")
    print("be considered as financial advice.")

if __name__ == "__main__":
    main()