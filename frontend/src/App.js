import React, { useState } from 'react';
import axios from 'axios';

/**
 * QUANTCODE Trading Analysis Application
 * =====================================
 * 
 * A complete React frontend for trading analysis using multiple technical indicators.
 * Features a modern dark theme with real-time analysis results display.
 * 
 * Author: QuantCode Team
 * Date: October 2025
 */

const App = () => {
  // State management using React hooks
  const [ticker, setTicker] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [hasAnalyzed, setHasAnalyzed] = useState(false);
  
  // Position Size Calculator state
  const [accountSize, setAccountSize] = useState('');
  const [entryPrice, setEntryPrice] = useState('');
  const [stopLossPrice, setStopLossPrice] = useState('');
  const [positionSizeLoading, setPositionSizeLoading] = useState(false);
  const [positionSizeResult, setPositionSizeResult] = useState(null);
  const [positionSizeError, setPositionSizeError] = useState(null);

  // API base URL - adjust this based on your Flask backend setup
  const API_BASE_URL = 'http://127.0.0.1:5000';

  /**
   * Handle the analysis request
   * Makes API call to Flask backend and updates component state
   */
  const handleAnalyze = async () => {
    // Validate ticker input
    if (!ticker.trim()) {
      setError('Please enter a valid ticker symbol');
      return;
    }

    // Reset previous states
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      // Make API call to Flask backend
      const response = await axios.get(
        `${API_BASE_URL}/analyze/${ticker.trim().toUpperCase()}`,
        {
          timeout: 30000, // 30 second timeout
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );

      // Update state with successful response
      setResults(response.data);
      setHasAnalyzed(true);
      
    } catch (err) {
      // Handle different types of errors
      if (err.response) {
        // API returned an error response
        setError(err.response.data.error || 'Analysis failed');
      } else if (err.request) {
        // Network error
        setError('Unable to connect to analysis server. Please check if the backend is running.');
      } else {
        // Other errors
        setError('An unexpected error occurred');
      }
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle Enter key press in input field
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleAnalyze();
    }
  };

  /**
   * Handle position size calculation
   * Makes API call to Flask backend for position sizing
   */
  const handleCalculatePositionSize = async () => {
    // Validate inputs
    if (!accountSize.trim() || !entryPrice.trim() || !stopLossPrice.trim()) {
      setPositionSizeError('Please fill in all fields');
      return;
    }

    const account = parseFloat(accountSize);
    const entry = parseFloat(entryPrice);
    const stopLoss = parseFloat(stopLossPrice);

    if (isNaN(account) || isNaN(entry) || isNaN(stopLoss)) {
      setPositionSizeError('Please enter valid numeric values');
      return;
    }

    if (account <= 0 || entry <= 0 || stopLoss <= 0) {
      setPositionSizeError('All values must be greater than 0');
      return;
    }

    // Reset previous states
    setPositionSizeLoading(true);
    setPositionSizeError(null);
    setPositionSizeResult(null);

    try {
      // Make API call to Flask backend for position size calculation
      const response = await axios.get(
        `${API_BASE_URL}/api/calculate_position_size`,
        {
          params: {
            account: account,
            risk: 1, // Hardcoded to 1% as requested
            entry: entry,
            sl: stopLoss
          },
          timeout: 10000, // 10 second timeout
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );

      // Update state with successful response
      setPositionSizeResult(response.data);
      
    } catch (err) {
      // Handle different types of errors
      if (err.response) {
        // API returned an error response
        setPositionSizeError(err.response.data.error || 'Position size calculation failed');
      } else if (err.request) {
        // Network error
        setPositionSizeError('Unable to connect to calculation server. Please check if the backend is running.');
      } else {
        // Other errors
        setPositionSizeError('An unexpected error occurred during calculation');
      }
      console.error('Position size calculation error:', err);
    } finally {
      setPositionSizeLoading(false);
    }
  };

  /**
   * Get signal color based on signal type
   */
  const getSignalColor = (signal) => {
    switch (signal?.toLowerCase()) {
      case 'buy': return '#00ff88';
      case 'sell': return '#ff4757';
      case 'hold': return '#ffa502';
      default: return '#70a1ff';
    }
  };

  /**
   * Get signal emoji based on signal type
   */
  const getSignalEmoji = (signal) => {
    switch (signal?.toLowerCase()) {
      case 'buy': return '📈';
      case 'sell': return '📉';
      case 'hold': return '⏸️';
      default: return '📊';
    }
  };

  /**
   * Format currency values
   */
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  };

  return (
    <div className="app">
      {/* Embedded CSS Styles */}
      <style jsx="true">{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
          color: #f0f0f0;
          min-height: 100vh;
        }

        .app {
          min-height: 100vh;
          background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
          padding: 20px;
          display: flex;
          flex-direction: column;
          align-items: center;
        }

        .header {
          text-align: center;
          margin-bottom: 40px;
          padding: 20px;
        }

        .title {
          font-size: 3.5rem;
          font-weight: 700;
          background: linear-gradient(45deg, #00ff88, #70a1ff, #ffa502);
          background-clip: text;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          margin-bottom: 10px;
          letter-spacing: 2px;
        }

        .subtitle {
          font-size: 1.2rem;
          color: #b0b0b0;
          font-weight: 300;
        }

        .input-section {
          background: rgba(255, 255, 255, 0.05);
          backdrop-filter: blur(10px);
          border-radius: 20px;
          padding: 30px;
          margin-bottom: 30px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
          min-width: 400px;
        }

        .input-group {
          display: flex;
          gap: 15px;
          align-items: center;
        }

        .ticker-input {
          flex: 1;
          padding: 15px 20px;
          background: rgba(255, 255, 255, 0.1);
          border: 2px solid rgba(255, 255, 255, 0.2);
          border-radius: 12px;
          color: #f0f0f0;
          font-size: 1.1rem;
          transition: all 0.3s ease;
          outline: none;
          text-transform: uppercase;
        }

        .ticker-input:focus {
          border-color: #70a1ff;
          box-shadow: 0 0 0 3px rgba(112, 161, 255, 0.2);
        }

        .ticker-input::placeholder {
          color: #888;
        }

        .analyze-btn {
          padding: 15px 30px;
          background: linear-gradient(45deg, #70a1ff, #5352ed);
          border: none;
          border-radius: 12px;
          color: white;
          font-size: 1.1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          box-shadow: 0 4px 15px rgba(112, 161, 255, 0.3);
        }

        .analyze-btn:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(112, 161, 255, 0.4);
        }

        .analyze-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
          transform: none;
        }

        .loading {
          text-align: center;
          padding: 40px;
          font-size: 1.2rem;
          color: #70a1ff;
        }

        .loading-spinner {
          display: inline-block;
          width: 20px;
          height: 20px;
          border: 3px solid rgba(112, 161, 255, 0.3);
          border-radius: 50%;
          border-top-color: #70a1ff;
          animation: spin 1s ease-in-out infinite;
          margin-right: 10px;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        .error {
          background: rgba(255, 71, 87, 0.1);
          border: 1px solid rgba(255, 71, 87, 0.3);
          border-radius: 12px;
          padding: 20px;
          margin: 20px 0;
          color: #ff4757;
          text-align: center;
          min-width: 400px;
        }

        .results {
          width: 100%;
          max-width: 800px;
          margin: 20px 0;
        }

        .main-result {
          background: rgba(255, 255, 255, 0.05);
          backdrop-filter: blur(10px);
          border-radius: 20px;
          padding: 30px;
          margin-bottom: 30px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
          text-align: center;
        }

        .ticker-display {
          font-size: 2rem;
          font-weight: 600;
          color: #70a1ff;
          margin-bottom: 15px;
        }

        .final-signal {
          font-size: 3rem;
          font-weight: 700;
          margin: 20px 0;
          text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        }

        .price-display {
          font-size: 1.5rem;
          color: #b0b0b0;
          margin-bottom: 15px;
        }

        .confidence {
          font-size: 1.1rem;
          color: #888;
          font-style: italic;
        }

        .analyses-section {
          background: rgba(255, 255, 255, 0.05);
          backdrop-filter: blur(10px);
          border-radius: 20px;
          padding: 30px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .section-title {
          font-size: 1.5rem;
          font-weight: 600;
          margin-bottom: 25px;
          color: #f0f0f0;
          text-align: center;
        }

        .analysis-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 20px;
        }

        .analysis-card {
          background: rgba(255, 255, 255, 0.05);
          border-radius: 15px;
          padding: 20px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          transition: transform 0.3s ease;
        }

        .analysis-card:hover {
          transform: translateY(-5px);
        }

        .analysis-header {
          display: flex;
          justify-content: between;
          align-items: center;
          margin-bottom: 15px;
        }

        .analysis-name {
          font-size: 1.2rem;
          font-weight: 600;
          color: #f0f0f0;
          text-transform: capitalize;
        }

        .analysis-signal {
          font-size: 1.1rem;
          font-weight: 700;
          padding: 5px 15px;
          border-radius: 20px;
          background: rgba(255, 255, 255, 0.1);
        }

        .analysis-details {
          color: #b0b0b0;
          font-size: 0.95rem;
          line-height: 1.4;
        }

        .signal-summary {
          background: rgba(255, 255, 255, 0.03);
          border-radius: 12px;
          padding: 20px;
          margin-top: 20px;
        }

        .signal-votes {
          display: flex;
          justify-content: space-around;
          align-items: center;
          text-align: center;
        }

        .vote-item {
          display: flex;
          flex-direction: column;
          align-items: center;
        }

        .vote-count {
          font-size: 2rem;
          font-weight: 700;
          margin-bottom: 5px;
        }

        .vote-label {
          font-size: 0.9rem;
          color: #888;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        @media (max-width: 768px) {
          .title {
            font-size: 2.5rem;
          }
          
          .input-section {
            min-width: 300px;
            padding: 20px;
          }
          
          .input-group {
            flex-direction: column;
          }
          
          .analysis-grid {
            grid-template-columns: 1fr;
          }
          
          .signal-votes {
            flex-direction: column;
            gap: 15px;
          }
        }
      `}</style>

      {/* Header Section */}
      <div className="header">
        <h1 className="title">QUANTCODE</h1>
        <p className="subtitle">Advanced Trading Analysis Platform</p>
      </div>

      {/* Input Section */}
      <div className="input-section">
        <div className="input-group">
          <input
            type="text"
            className="ticker-input"
            placeholder="Enter ticker (e.g., AAPL, RELIANCE.NS)"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
          />
          <button
            className="analyze-btn"
            onClick={handleAnalyze}
            disabled={loading || !ticker.trim()}
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </div>

      {/* Position Size Calculator */}
      <div className="position-calculator">
        <h2 className="calculator-title">Position Size Calculator</h2>
        
        <div className="calculator-inputs">
          <div className="input-field">
            <label className="input-label">Account Size (INR)</label>
            <input
              type="number"
              className="calculator-input"
              placeholder="Enter your account size"
              value={accountSize}
              onChange={(e) => setAccountSize(e.target.value)}
            />
          </div>
          
          <div className="input-field">
            <label className="input-label">Entry Price</label>
            <input
              type="number"
              step="0.01"
              className="calculator-input"
              placeholder="Enter entry price"
              value={entryPrice}
              onChange={(e) => setEntryPrice(e.target.value)}
            />
          </div>
          
          <div className="input-field">
            <label className="input-label">Stop Loss Price</label>
            <input
              type="number"
              step="0.01"
              className="calculator-input"
              placeholder="Enter stop loss price"
              value={stopLossPrice}
              onChange={(e) => setStopLossPrice(e.target.value)}
            />
          </div>
        </div>
        
        <button
          className="calculate-btn"
          onClick={handleCalculatePositionSize}
          disabled={positionSizeLoading || !accountSize.trim() || !entryPrice.trim() || !stopLossPrice.trim()}
        >
          {positionSizeLoading ? (
            <>
              <div className="loading-spinner"></div>
              Calculating...
            </>
          ) : (
            'Calculate Position Size'
          )}
        </button>
        
        {/* Position Size Error Display */}
        {positionSizeError && (
          <div className="position-error">
            <strong>Error:</strong> {positionSizeError}
          </div>
        )}
        
        {/* Position Size Result Display */}
        {positionSizeResult && !positionSizeLoading && (
          <div className="position-result">
            <div className="position-result-title">Recommended Position Size</div>
            <div className="position-result-value">
              {positionSizeResult.calculation?.max_shares || 0} shares/lots
            </div>
            <div className="position-result-details">
              <div>Risk Amount: ₹{positionSizeResult.calculation?.risk_amount || 0}</div>
              <div>Total Investment: ₹{positionSizeResult.recommendation?.total_investment || 0}</div>
              <div>Risk per Share: ₹{positionSizeResult.calculation?.risk_per_share || 0}</div>
              <div style={{ marginTop: '10px', fontStyle: 'italic' }}>
                Using 1% risk rule - Max loss if stop loss hit: ₹{positionSizeResult.calculation?.risk_amount || 0}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Loading Indicator */}
      {loading && (
        <div className="loading">
          <div className="loading-spinner"></div>
          Analyzing {ticker.toUpperCase()}... Please wait
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Results Display */}
      {results && hasAnalyzed && !loading && (
        <div className="results">
          {/* Main Result Card */}
          <div className="main-result">
            <div className="ticker-display">
              {results.ticker}
            </div>
            <div className="price-display">
              {formatCurrency(results.latest_close_price)}
            </div>
            <div 
              className="final-signal"
              style={{ color: getSignalColor(results.final_signal) }}
            >
              {getSignalEmoji(results.final_signal)} {results.final_signal}
            </div>
            <div className="confidence">
              {results.confidence}
            </div>
          </div>

          {/* Detailed Analyses */}
          <div className="analyses-section">
            <h2 className="section-title">Technical Analysis Breakdown</h2>
            
            <div className="analysis-grid">
              {Object.entries(results.analyses || {}).map(([key, analysis]) => (
                <div key={key} className="analysis-card">
                  <div className="analysis-header">
                    <div className="analysis-name">
                      {key.replace('_', ' ')}
                    </div>
                    <div 
                      className="analysis-signal"
                      style={{ color: getSignalColor(analysis.signal) }}
                    >
                      {getSignalEmoji(analysis.signal)} {analysis.signal}
                    </div>
                  </div>
                  <div className="analysis-details">
                    {analysis.details}
                  </div>
                </div>
              ))}
            </div>

            {/* Signal Summary */}
            {results.signal_summary && (
              <div className="signal-summary">
                <h3 className="section-title">Signal Consensus</h3>
                <div className="signal-votes">
                  <div className="vote-item">
                    <div 
                      className="vote-count"
                      style={{ color: getSignalColor('buy') }}
                    >
                      {results.signal_summary.buy_votes}
                    </div>
                    <div className="vote-label">Buy Votes</div>
                  </div>
                  <div className="vote-item">
                    <div 
                      className="vote-count"
                      style={{ color: getSignalColor('sell') }}
                    >
                      {results.signal_summary.sell_votes}
                    </div>
                    <div className="vote-label">Sell Votes</div>
                  </div>
                  <div className="vote-item">
                    <div 
                      className="vote-count"
                      style={{ color: getSignalColor('hold') }}
                    >
                      {results.signal_summary.hold_votes}
                    </div>
                    <div className="vote-label">Hold Votes</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;