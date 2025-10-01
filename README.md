# QUANTCODE Trading Analysis Platform

A professional full-stack trading analysis application that implements multiple technical indicators and provides decisive trading signals through a modern web interface.

## 🚀 **Full-Stack Architecture**

- **Backend**: Flask API with Python-based technical analysis
- **Frontend**: Modern React application with dark theme
- **Analysis Engine**: Multi-indicator consensus system
- **Real-time Data**: Yahoo Finance integration

## ⚡ **Quick Start**

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### 1. Clone & Setup
```bash
git clone <repository-url>
cd QuantCode
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start Flask API
python app.py
```
**Backend running at:** `http://localhost:5000`

### 3. Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start React app
npm start
```
**Frontend running at:** `http://localhost:3000`

## 📊 **Features**

### **Backend (Flask API)**
- **Multi-Indicator Analysis**: Heiken Ashi, Bollinger Bands, MACD, RSI
- **Consensus Signals**: Majority voting system for final recommendations
- **RESTful API**: Comprehensive endpoints for all analysis types
- **Error Handling**: Robust validation and error management
- **Batch Processing**: Analyze multiple tickers simultaneously

### **Frontend (React App)**
- **Modern Dark Theme**: Professional trading interface
- **Real-time Analysis**: Live updates with loading states
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive UI**: Smooth animations and hover effects
- **Error Management**: User-friendly error messages

## 🎯 **Signal Generation Logic**

### **Final Signal Determination**
- **BUY**: ≥2 indicators vote BUY and BUY > SELL votes
- **SELL**: ≥2 indicators vote SELL and SELL > BUY votes  
- **HOLD**: Mixed signals or no clear majority

### **Individual Indicators**
- **Heiken Ashi**: Decisive candle patterns
- **Bollinger Bands**: Overbought/oversold conditions
- **MACD**: Momentum and trend analysis
- **RSI**: Relative strength analysis

## 📱 **User Interface**

### **Main Features**
- Ticker input with real-time validation
- One-click analysis with loading indicators
- Comprehensive results display
- Signal consensus voting breakdown
- Individual indicator details

### **Design Elements**
- Modern gradient backgrounds
- Glass morphism effects
- Responsive grid layouts
- Signal-based color coding
- Smooth animations

## 🔗 **API Endpoints**

### **Core Analysis**
- `GET /analyze/<ticker>` - Comprehensive multi-indicator analysis
- `GET /health` - API health check

### **Individual Indicators**
- `GET /analyze/<ticker>/heiken-ashi` - Heiken Ashi analysis
- `GET /analyze/<ticker>/bollinger` - Bollinger Bands analysis
- `GET /analyze/<ticker>/macd` - MACD analysis
- `GET /analyze/<ticker>/rsi` - RSI analysis

### **Batch Processing**
- `POST /batch-analyze` - Multiple ticker analysis

## 📈 **Sample Response**

```json
{
  "ticker": "AAPL",
  "final_signal": "HOLD",
  "confidence": "Mixed signals - no clear consensus",
  "latest_close_price": 254.63,
  "analyses": {
    "heiken_ashi": {
      "signal": "HOLD",
      "details": "Bullish candle with lower wick - Mixed signals"
    },
    "bollinger_bands": {
      "signal": "HOLD", 
      "details": "Price above SMA (79.8%) - Bullish bias"
    },
    "macd": {
      "signal": "HOLD",
      "details": "MACD above Signal line - Bullish momentum"
    },
    "rsi": {
      "signal": "SELL",
      "details": "RSI 82.8 - Overbought condition"
    }
  }
}
```

## 🛠️ **Technology Stack**

### **Backend**
- **Python 3.8+**: Core programming language
- **Flask**: Web framework and API server
- **pandas**: Data manipulation and analysis
- **yfinance**: Yahoo Finance data integration
- **numpy**: Numerical computations

### **Frontend**
- **React 18**: Modern UI framework
- **Axios**: HTTP client for API communication
- **CSS3**: Modern styling with gradients and animations
- **ES6+**: Modern JavaScript features

## 📚 **Documentation**

- **[Full-Stack Setup Guide](FULLSTACK_SETUP.md)**: Complete installation instructions
- **[Flask Integration Guide](FLASK_INTEGRATION.md)**: Backend API documentation
- **[Technical Documentation](TECHNICAL_DOCS.md)**: Detailed technical specifications

## 🧪 **Testing**

### **Backend Testing**
```bash
python test_analyzer.py
```

### **API Testing**
```bash
curl http://localhost:5000/analyze/AAPL
```

### **Frontend Testing**
- Open `http://localhost:3000`
- Test with sample tickers: AAPL, TSLA, RELIANCE.NS

## 🌍 **Market Coverage**

### **Supported Markets**
- **US Stocks**: AAPL, TSLA, MSFT, GOOGL, AMZN
- **Indian Stocks**: RELIANCE.NS, TCS.NS, INFY.NS
- **International**: Most Yahoo Finance supported tickers

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Backend
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000

# Frontend  
REACT_APP_API_URL=http://localhost:5000
```

## 📄 **License**

See LICENSE file for details.

## ⚠️ **Disclaimer**

This application is for educational and analytical purposes only. Trading signals should not be considered as financial advice. Always conduct your own research and consider consulting with financial professionals before making investment decisions.

---

**🚀 Ready for Production**: Complete full-stack trading analysis platform with modern web interface!