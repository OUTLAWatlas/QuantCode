import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Grid } from '@mui/material';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import ChartView from './components/ChartView';
import RiskCalculator from './components/RiskCalculator';
import AnalysisView from './components/AnalysisView';
import SkeletonLoader from './components/SkeletonLoader';
import TickerManager from './components/TickerManager';
import JournalView from './components/JournalView';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';
import './styles/singularity.css';

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
  // Core state
  const [selectedTicker, setSelectedTicker] = useState('RELIANCE.NS');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  // Focus mode
  const [isFocusMode, setIsFocusMode] = useState(false);
  const toggleFocusMode = () => setIsFocusMode(v => !v);

  // Dashboard summaries and chart series
  const [TICKERS, setTICKERS] = useState(['RELIANCE.NS', 'INFY.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS']);
  const [summaries, setSummaries] = useState({});
  const [chartSeries, setChartSeries] = useState([]);
  const [chartData, setChartData] = useState(null);
  const [settingsOpen, setSettingsOpen] = useState(false);

  // Journal view state
  const [activeView, setActiveView] = useState('dashboard'); // 'dashboard' or 'journal'

  // API base URL - adjust this based on your Flask backend setup
  const API_BASE_URL = 'http://127.0.0.1:5000';

  // Helpers (kept minimal in App; components handle their own formatting)

  /**
   * Handle the analysis request
   * Makes API call to Flask backend and updates component state
   */
  const fetchAnalysis = async (ticker) => {
    setLoading(true); setResults(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/analyze/${ticker}`, { timeout: 30000 });
      const data = response.data;
      setResults(data);
      // If backend provides chart_data with close, prefer it and skip separate history call
      if (data && data.chart_data && Array.isArray(data.chart_data.close) && data.chart_data.close.length > 0) {
        setChartData(data.chart_data);
        setChartSeries(data.chart_data.close);
      } else {
        setChartData(null);
      }
    } catch (err) {
    } finally { setLoading(false); }
  };

  const fetchDashboardSummaries = async () => {
    const entries = await Promise.all(TICKERS.map(async (t) => {
      try {
        const r = await axios.get(`${API_BASE_URL}/analyze/${t}`, { timeout: 25000 });
        return [t, { final_signal: r.data.final_signal }];
      } catch { return [t, { final_signal: 'N/A' }]; }
    }));
    setSummaries(Object.fromEntries(entries));
  };

  // NOTE: Backend may not expose historical OHLC endpoint; attempt and fallback to empty series
  const fetchHistory = async (ticker) => {
    try {
      const r = await axios.get(`${API_BASE_URL}/api/history/${ticker}`, { timeout: 20000 });
      // Expecting array of { time: 'YYYY-MM-DD', value: number }
      if (Array.isArray(r.data?.series)) return r.data.series;
    } catch {}
    return [];
  };

  // (Logic centralized here; components encapsulate presentation)

  // On mount: fetch summaries and default ticker
  useEffect(() => {
    fetchDashboardSummaries();
    fetchAnalysis(selectedTicker);
    (async () => {
      // Only fetch history if we don't get close series from analysis
      if (!chartData) {
        setChartSeries(await fetchHistory(selectedTicker));
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // On ticker change: refetch detailed analysis and chart
  useEffect(() => {
    if (!selectedTicker) return;
    fetchAnalysis(selectedTicker);
    (async () => {
      if (!chartData) {
        setChartSeries(await fetchHistory(selectedTicker));
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedTicker]);

  // Load watchlist from API on mount
  useEffect(() => {
    (async () => {
      try {
        const r = await axios.get(`${API_BASE_URL}/api/tickers`, { timeout: 15000 });
        if (Array.isArray(r.data) && r.data.length) {
          setTICKERS(r.data);
        }
      } catch {}
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleTickersSaved = (list) => {
    if (Array.isArray(list) && list.length) {
      setTICKERS(list);
      // Refresh summaries for new watchlist
      fetchDashboardSummaries();
      // If current selectedTicker not in list, switch to first
      if (!list.includes(selectedTicker)) {
        setSelectedTicker(list[0]);
      }
    }
    setSettingsOpen(false);
  };

  // --- Navigation ---
  const handleNav = (view) => setActiveView(view);

  return (
    <div className={`app app-bg ${isFocusMode ? 'focus-mode-active' : ''}`}>
      <div className="data-streams" aria-hidden>
        <div className="stream" /><div className="stream" /><div className="stream" /><div className="stream" />
      </div>
      {/* Header with Journal button */}
      <Header focusMode={isFocusMode} onToggleFocus={toggleFocusMode}>
        <Button
          variant={activeView === 'dashboard' ? 'outlined' : 'contained'}
          sx={{ ml: 2, background: activeView === 'journal' ? '#39FF14' : undefined, color: activeView === 'journal' ? '#181A20' : undefined, fontWeight: 'bold' }}
          onClick={() => handleNav(activeView === 'journal' ? 'dashboard' : 'journal')}
        >
          {activeView === 'journal' ? 'Back to Dashboard' : 'Journal'}
        </Button>
      </Header>

      <Container maxWidth="xl" sx={{ mt: 3, mb: 6 }}>
        {activeView === 'dashboard' ? (
          <div className={`main-grid ${isFocusMode ? 'focus-mode' : ''}`}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={3} className="dashboard-panel">
                <Dashboard tickers={TICKERS} summaries={summaries} loading={loading} selected={selectedTicker} onSelect={setSelectedTicker} />
                <Button variant="outlined" size="small" sx={{ mt: 2 }} className="btn-glow" onClick={() => setSettingsOpen(true)}>
                  Manage Tickers
                </Button>
              </Grid>
              <Grid item xs={12} md={6} className="chart-view-panel">
                <Grid container spacing={3}>
                  <Grid item xs={12}>
                    <ChartView ticker={selectedTicker} chartData={chartData || { close: chartSeries }} />
                  </Grid>
                  <Grid item xs={12}>
                    {loading && <SkeletonLoader />}
                    {!loading && results && <AnalysisView analysisData={results} />}
                  </Grid>
                </Grid>
              </Grid>
              <Grid item xs={12} md={3} className="risk-calculator-panel">
                <RiskCalculator apiBase={API_BASE_URL} />
              </Grid>
            </Grid>
          </div>
        ) : (
          <JournalView />
        )}
      </Container>

      <Dialog open={settingsOpen} onClose={() => setSettingsOpen(false)} fullWidth maxWidth="sm">
        <DialogTitle className="title-orbitron">Manage Watchlist</DialogTitle>
        <DialogContent>
          <TickerManager apiBase={API_BASE_URL} onSaved={handleTickersSaved} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSettingsOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default App;