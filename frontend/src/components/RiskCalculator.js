import React, { useState } from 'react';
import { Card, CardHeader, CardContent, Grid, TextField, Stack, Chip, Alert, Typography, Divider, Box, InputAdornment } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import { Functions } from '@mui/icons-material';
import axios from 'axios';

const RiskCalculator = ({ apiBase = 'http://127.0.0.1:5000' }) => {
  const [accountSize, setAccountSize] = useState('');
  const [entryPrice, setEntryPrice] = useState('');
  const [stopLossPrice, setStopLossPrice] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const isInvalid = (v) => v === '' || isNaN(Number(v)) || Number(v) <= 0;

  const formatInr = (value) => {
    if (value === null || value === undefined || isNaN(value)) return '₹0.00';
    try {
      return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Number(value));
    } catch {
      return `₹${Number(value).toFixed(2)}`;
    }
  };

  const calculate = async () => {
    if (isInvalid(accountSize) || isInvalid(entryPrice) || isInvalid(stopLossPrice)) {
      setError('Please enter valid values (> 0)');
      return;
    }
    setLoading(true); setError(null); setResult(null);
    try {
      const response = await axios.get(`${apiBase}/api/calculate_position_size`, {
        params: { account: Number(accountSize), risk: 1, entry: Number(entryPrice), sl: Number(stopLossPrice) },
        timeout: 10000,
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Calculation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="panel panel-frosted">
      <CardHeader title="Risk Calculator" subheader="1% risk per trade" className="panel-header" />
      <CardContent>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <TextField label="Account Size (INR)" type="number" value={accountSize} onChange={(e) => setAccountSize(e.target.value)} error={isInvalid(accountSize)} helperText={isInvalid(accountSize) ? 'Enter a value > 0' : ' '} InputProps={{ startAdornment: <InputAdornment position="start">₹</InputAdornment> }} />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField label="Entry Price" type="number" value={entryPrice} onChange={(e) => setEntryPrice(e.target.value)} error={isInvalid(entryPrice)} helperText={isInvalid(entryPrice) ? 'Enter a value > 0' : ' '} InputProps={{ startAdornment: <InputAdornment position="start">₹</InputAdornment> }} />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField label="Stop Loss" type="number" value={stopLossPrice} onChange={(e) => setStopLossPrice(e.target.value)} error={isInvalid(stopLossPrice)} helperText={isInvalid(stopLossPrice) ? 'Enter a value > 0' : ' '} InputProps={{ startAdornment: <InputAdornment position="start">₹</InputAdornment> }} />
          </Grid>
          <Grid item xs={12}>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <LoadingButton className="btn-glow" startIcon={<Functions />} onClick={calculate} loading={loading} disabled={isInvalid(accountSize) || isInvalid(entryPrice) || isInvalid(stopLossPrice)}>Calculate</LoadingButton>
              <Chip label="Risk: 1%" className="chip-outline" />
            </Stack>
          </Grid>
          {error && (
            <Grid item xs={12}><Alert severity="error" className="glitch-in">{error}</Alert></Grid>
          )}
          {result && !loading && (
            <Grid item xs={12}>
              <Card className="result-card hex-pulse">
                <CardContent>
                  <Typography variant="h6" className="neon-green" gutterBottom>Recommended Position Size</Typography>
                  <Typography variant="h3" className="neon-green" gutterBottom>{result.calculation?.max_shares || 0} shares/lots</Typography>
                  <Divider sx={{ my: 2 }} />
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={4}><Typography variant="body2" color="text.secondary">Risk Amount</Typography><Typography variant="body1">{formatInr(result.calculation?.risk_amount || 0)}</Typography></Grid>
                    <Grid item xs={12} sm={4}><Typography variant="body2" color="text.secondary">Total Investment</Typography><Typography variant="body1">{formatInr(result.recommendation?.total_investment || 0)}</Typography></Grid>
                    <Grid item xs={12} sm={4}><Typography variant="body2" color="text.secondary">Risk per Share</Typography><Typography variant="body1">{formatInr(result.calculation?.risk_per_share || 0)}</Typography></Grid>
                  </Grid>
                  <Box mt={2}><Typography variant="caption" color="text.secondary" fontStyle="italic">Using 1% risk rule</Typography></Box>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      </CardContent>
    </Card>
  );
};

export default RiskCalculator;
