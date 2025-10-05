import React, { useEffect, useState } from 'react';
import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Paper, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Typography, Chip
} from '@mui/material';
import { styled } from '@mui/material/styles';

// Neon color palette for Project Singularity aesthetic
const NeonGreen = '#39FF14';
const NeonRed = '#FF073A';
const NeonBlue = '#00FFFF';
const NeonGray = '#222831';
const NeonBg = '#181A20';

const StatusChip = styled(Chip)(({ status }) => ({
  backgroundColor: status === 'OPEN' ? NeonGreen : NeonRed,
  color: NeonGray,
  fontWeight: 'bold',
  fontSize: '1em',
}));

const PnLCell = styled(TableCell)(({ value }) => ({
  color: value > 0 ? NeonGreen : value < 0 ? NeonRed : NeonBlue,
  fontWeight: 'bold',
  fontSize: '1em',
}));

function calcPnL(trade) {
  if (trade.status !== 'CLOSED' || trade.exit_price == null) return null;
  const entry = parseFloat(trade.entry_price);
  const exit = parseFloat(trade.exit_price);
  if (trade.trade_type === 'LONG') return exit - entry;
  if (trade.trade_type === 'SHORT') return entry - exit;
  return null;
}

export default function JournalView() {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedTrade, setSelectedTrade] = useState(null);
  const [exitPrice, setExitPrice] = useState('');
  const [closing, setClosing] = useState(false);
  const [error, setError] = useState('');

  const fetchTrades = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/trades');
      const data = await res.json();
      setTrades(Array.isArray(data) ? data : []);
    } catch (e) {
      setTrades([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchTrades();
  }, []);

  const handleCloseTrade = (trade) => {
    setSelectedTrade(trade);
    setExitPrice('');
    setError('');
    setModalOpen(true);
  };

  const handleModalClose = () => {
    setModalOpen(false);
    setSelectedTrade(null);
    setExitPrice('');
    setError('');
  };

  const handleConfirmClose = async () => {
    if (!exitPrice || isNaN(exitPrice)) {
      setError('Please enter a valid exit price.');
      return;
    }
    setClosing(true);
    try {
      const res = await fetch(`/api/trades/${selectedTrade.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exit_price: parseFloat(exitPrice) })
      });
      if (res.ok) {
        handleModalClose();
        fetchTrades();
      } else {
        const err = await res.json();
        setError(err.error || 'Failed to close trade.');
      }
    } catch (e) {
      setError('Network error.');
    }
    setClosing(false);
  };

  return (
    <Paper sx={{ background: NeonBg, p: 3, minHeight: '80vh' }} elevation={6}>
      <Typography variant="h4" sx={{ color: NeonGreen, mb: 2, fontWeight: 'bold', letterSpacing: 2 }}>
        Trading Journal
      </Typography>
      <TableContainer component={Paper} sx={{ background: NeonGray }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell sx={{ color: NeonBlue, fontWeight: 'bold' }}>Ticker</TableCell>
              <TableCell sx={{ color: NeonBlue, fontWeight: 'bold' }}>Type</TableCell>
              <TableCell sx={{ color: NeonBlue, fontWeight: 'bold' }}>Entry Price</TableCell>
              <TableCell sx={{ color: NeonBlue, fontWeight: 'bold' }}>Entry Date</TableCell>
              <TableCell sx={{ color: NeonBlue, fontWeight: 'bold' }}>Status</TableCell>
              <TableCell sx={{ color: NeonBlue, fontWeight: 'bold' }}>Exit Price</TableCell>
              <TableCell sx={{ color: NeonBlue, fontWeight: 'bold' }}>P&amp;L</TableCell>
              <TableCell sx={{ color: NeonBlue, fontWeight: 'bold' }}>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={8} align="center" sx={{ color: NeonBlue }}>
                  Loading trades...
                </TableCell>
              </TableRow>
            ) : trades.length === 0 ? (
              <TableRow>
                <TableCell colSpan={8} align="center" sx={{ color: NeonBlue }}>
                  No trades found.
                </TableCell>
              </TableRow>
            ) : (
              trades.map(trade => {
                const pnl = calcPnL(trade);
                return (
                  <TableRow key={trade.id}>
                    <TableCell sx={{ color: NeonGreen }}>{trade.ticker_symbol}</TableCell>
                    <TableCell sx={{ color: NeonBlue }}>{trade.trade_type}</TableCell>
                    <TableCell sx={{ color: NeonBlue }}>{trade.entry_price}</TableCell>
                    <TableCell sx={{ color: NeonBlue }}>{new Date(trade.entry_timestamp).toLocaleString()}</TableCell>
                    <TableCell>
                      <StatusChip label={trade.status} status={trade.status} />
                    </TableCell>
                    <TableCell sx={{ color: NeonBlue }}>{trade.exit_price ?? '-'}</TableCell>
                    <PnLCell value={pnl}>{pnl !== null ? pnl.toFixed(2) : '-'}</PnLCell>
                    <TableCell>
                      {trade.status === 'OPEN' ? (
                        <Button
                          variant="contained"
                          sx={{ background: NeonBlue, color: NeonGray, fontWeight: 'bold' }}
                          onClick={() => handleCloseTrade(trade)}
                        >
                          Close Trade
                        </Button>
                      ) : (
                        <Typography sx={{ color: NeonBlue }}>-</Typography>
                      )}
                    </TableCell>
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <Dialog open={modalOpen} onClose={handleModalClose}>
        <DialogTitle sx={{ color: NeonGreen, background: NeonGray }}>
          Close Trade
        </DialogTitle>
        <DialogContent sx={{ background: NeonGray }}>
          {selectedTrade && (
            <>
              <Typography sx={{ color: NeonBlue, mb: 1 }}>
                <strong>Ticker:</strong> {selectedTrade.ticker_symbol}
              </Typography>
              <Typography sx={{ color: NeonBlue, mb: 1 }}>
                <strong>Entry Price:</strong> {selectedTrade.entry_price}
              </Typography>
              <TextField
                label="Exit Price"
                type="number"
                fullWidth
                value={exitPrice}
                onChange={e => setExitPrice(e.target.value)}
                sx={{ mt: 2, input: { color: NeonGreen } }}
                InputLabelProps={{ style: { color: NeonBlue } }}
              />
              {error && (
                <Typography sx={{ color: NeonRed, mt: 1 }}>{error}</Typography>
              )}
            </>
          )}
        </DialogContent>
        <DialogActions sx={{ background: NeonGray }}>
          <Button onClick={handleModalClose} sx={{ color: NeonBlue }}>Cancel</Button>
          <Button
            onClick={handleConfirmClose}
            disabled={closing}
            sx={{ background: NeonGreen, color: NeonGray, fontWeight: 'bold' }}
          >
            Confirm Close
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
  );
}
