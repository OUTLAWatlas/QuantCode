# QuantCode Full-Stack Setup Guide

## 🚀 Complete Application Architecture

```
QuantCode/
├── Backend (Flask API)
│   ├── backend/
│   │   └── quantcode_analyzer.py     # Core analysis class
│   ├── app.py                        # Flask API server
│   ├── requirements.txt              # Python dependencies
│   └── .venv/                        # Python virtual environment
│
├── Frontend (React App)
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   └── index.js             # React entry point
│   ├── public/
│   │   └── index.html           # HTML template
│   ├── package.json             # Node dependencies
│   └── node_modules/            # Node packages
│
└── Documentation
    ├── README.md                # Project overview
    ├── FLASK_INTEGRATION.md     # Backend documentation
    └── TECHNICAL_DOCS.md        # Technical specifications
```

## 📋 Prerequisites

- **Python 3.8+**: For backend Flask API
- **Node.js 16+**: For React frontend
- **npm or yarn**: Package manager for React
- **Git**: Version control (optional)

## 🛠️ Backend Setup (Flask API)

### 1. Navigate to Project Root
```bash
cd QuantCode
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Flask Backend
```bash
python app.py
```

**Backend will be running at:** `http://localhost:5000`

### 5. Test Backend API
```bash
# Test with curl
curl http://localhost:5000/analyze/AAPL

# Or visit in browser
http://localhost:5000
```

## ⚛️ Frontend Setup (React App)

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Node Dependencies
```bash
npm install
```

### 3. Start React Development Server
```bash
npm start
```

**Frontend will be running at:** `http://localhost:3000`

## 🔗 Full-Stack Integration

### API Endpoint Configuration

The React frontend is configured to call the Flask backend at:
```
http://127.0.0.1:5000/analyze/{ticker}
```

### CORS Setup (if needed)

If you encounter CORS issues, add this to your Flask `app.py`:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

Then install flask-cors:
```bash
pip install flask-cors
```

## 🚀 Quick Start (Both Services)

### Terminal 1 - Backend
```bash
cd QuantCode
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
python app.py
```

### Terminal 2 - Frontend
```bash
cd QuantCode/frontend
npm start
```

## 📱 Usage Instructions

1. **Start both services** (backend + frontend)
2. **Open browser** to `http://localhost:3000`
3. **Enter a ticker symbol** (e.g., AAPL, TSLA, RELIANCE.NS)
4. **Click "Analyze"** or press Enter
5. **View comprehensive results** with multiple technical indicators

## 🎯 Sample Test Cases

Try these ticker symbols to test the application:

### US Stocks
- **AAPL** - Apple Inc.
- **TSLA** - Tesla Inc.
- **MSFT** - Microsoft Corp.
- **GOOGL** - Alphabet Inc.
- **AMZN** - Amazon.com Inc.

### Indian Stocks
- **RELIANCE.NS** - Reliance Industries
- **TCS.NS** - Tata Consultancy Services
- **INFY.NS** - Infosys Limited
- **ICICIBANK.NS** - ICICI Bank

## 🔧 Configuration Options

### Backend Configuration (app.py)
```python
# API settings
API_BASE_URL = 'http://127.0.0.1:5000'
DEBUG_MODE = True
PORT = 5000

# Analysis settings
DEFAULT_DAYS = 100
MAX_BATCH_SIZE = 10
```

### Frontend Configuration (App.js)
```javascript
// API configuration
const API_BASE_URL = 'http://127.0.0.1:5000';

// Timeout settings
timeout: 30000  // 30 seconds
```

## 📊 API Endpoints

### Core Analysis
- `GET /` - API documentation
- `GET /analyze/<ticker>` - Comprehensive analysis
- `GET /health` - Health check

### Individual Indicators
- `GET /analyze/<ticker>/heiken-ashi` - Heiken Ashi only
- `GET /analyze/<ticker>/bollinger` - Bollinger Bands only
- `GET /analyze/<ticker>/macd` - MACD only
- `GET /analyze/<ticker>/rsi` - RSI only

### Batch Processing
- `POST /batch-analyze` - Multiple tickers

### Query Parameters
- `?days=100` - Historical data period
- `?window=20` - Moving average window
- `?std_dev=2` - Bollinger Bands standard deviation

## 🛡️ Error Handling

### Backend Errors
- **400**: Invalid ticker or parameters
- **500**: Server or data processing errors

### Frontend Errors
- **Network errors**: Backend not running
- **Validation errors**: Empty ticker input
- **Timeout errors**: API response too slow

## 🏗️ Production Deployment

### Backend (Flask)
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend (React)
```bash
# Build for production
npm run build

# Serve static files
npm install -g serve
serve -s build -l 3000
```

## 📈 Performance Tips

### Backend Optimization
- Use Redis for caching frequently requested tickers
- Implement connection pooling for database operations
- Add rate limiting for API endpoints

### Frontend Optimization
- Implement debouncing for ticker input
- Add local caching for analysis results
- Use React.memo for performance optimization

## 🔍 Troubleshooting

### Common Issues

1. **Backend not starting**
   - Check Python version (3.8+)
   - Verify virtual environment activation
   - Install missing dependencies

2. **Frontend API calls failing**
   - Ensure backend is running on port 5000
   - Check CORS configuration
   - Verify API URL in frontend code

3. **Analysis errors**
   - Check internet connectivity (for Yahoo Finance data)
   - Verify ticker symbol format
   - Ensure sufficient historical data available

### Debug Commands

```bash
# Check backend status
curl http://localhost:5000/health

# Check Python packages
pip list

# Check Node packages
npm list

# View backend logs
python app.py  # Check console output

# View frontend logs
npm start  # Check browser console
```

## 🎉 Success Indicators

When everything is working correctly, you should see:

✅ **Backend**: Flask server running on port 5000  
✅ **Frontend**: React app running on port 3000  
✅ **API**: Successful ticker analysis with JSON response  
✅ **UI**: Modern dark theme with real-time results  
✅ **Integration**: Smooth communication between frontend and backend  

---

**🚀 Your QuantCode Trading Analysis Platform is now ready for use!**