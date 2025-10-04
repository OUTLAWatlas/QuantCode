import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Box,
  Stack,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Alert,
  Divider,
} from '@mui/material';
import { Delete, Add } from '@mui/icons-material';

const TickerManager = ({ apiBase = 'http://127.0.0.1:5000', onSaved }) => {
  const [tickers, setTickers] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    let ignore = false;
    const fetchTickers = async () => {
      setLoading(true); setError(null);
      try {
        const r = await axios.get(`${apiBase}/api/tickers`, { timeout: 15000 });
        if (!ignore && Array.isArray(r.data)) {
          setTickers(r.data);
        }
      } catch (e) {
        if (!ignore) setError('Failed to load tickers.');
      } finally {
        if (!ignore) setLoading(false);
      }
    };
    fetchTickers();
    return () => { ignore = true; };
  }, [apiBase]);

  const addTicker = () => {
    const sym = (input || '').trim().toUpperCase();
    if (!sym) return;
    if (!tickers.includes(sym)) setTickers((prev) => [...prev, sym]);
    setInput('');
  };

  const removeTicker = (sym) => {
    setTickers((prev) => prev.filter((t) => t !== sym));
  };

  const saveChanges = async () => {
    setLoading(true); setError(null); setSuccess(null);
    try {
      await axios.post(`${apiBase}/api/tickers`, { tickers }, { timeout: 20000, headers: { 'Content-Type': 'application/json' } });
      setSuccess('Watchlist updated.');
      if (typeof onSaved === 'function') onSaved(tickers);
    } catch (e) {
      setError('Failed to save tickers.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <TextField
          label="Add Ticker"
          size="small"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') addTicker(); }}
          placeholder="e.g., AAPL, RELIANCE.NS"
          fullWidth
        />
        <Button variant="contained" className="btn-glow" onClick={addTicker} startIcon={<Add />} disabled={loading}>
          Add
        </Button>
      </Stack>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

      <List dense sx={{ maxHeight: 300, overflowY: 'auto', borderRadius: 1, border: '1px solid rgba(255,255,255,0.08)' }}>
        {tickers.length === 0 && (
          <ListItem><ListItemText primary="No tickers yet." secondary="Add your first ticker above." /></ListItem>
        )}
        {tickers.map((sym) => (
          <ListItem key={sym}
            secondaryAction={
              <IconButton edge="end" aria-label="remove" onClick={() => removeTicker(sym)} disabled={loading}>
                <Delete />
              </IconButton>
            }
          >
            <ListItemText primary={sym} />
          </ListItem>
        ))}
      </List>

      <Divider sx={{ my: 2, opacity: 0.3 }} />

      <Stack direction="row" justifyContent="flex-end">
        <Button variant="outlined" onClick={saveChanges} disabled={loading} className="btn-glow">
          Save Changes
        </Button>
      </Stack>
    </Box>
  );
};

export default TickerManager;
