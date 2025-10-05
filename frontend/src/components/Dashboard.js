
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardHeader, CardContent, List, ListItemButton, ListItemText, Chip, Stack } from '@mui/material';

const signalToChip = (signal) => {
  const s = (signal || '').toLowerCase();
  if (s === 'buy') return { label: 'BUY', className: 'chip-buy' };
  if (s === 'sell') return { label: 'SELL', className: 'chip-sell' };
  if (s === 'hold') return { label: 'HOLD', className: 'chip-hold' };
  return { label: 'N/A', className: 'chip-neutral' };
};

const Dashboard = ({ onSelect, selected }) => {
  const [loading, setLoading] = useState(true);
  const [summaries, setSummaries] = useState([]);

  useEffect(() => {
    const fetchDashboard = async () => {
      setLoading(true);
      try {
        const response = await axios.get('/api/dashboard');
        setSummaries(response.data);
      } catch (err) {
        setSummaries([]);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  return (
    <Card className="panel panel-frosted">
      <CardHeader title="Dashboard" subheader="Watchlist" className="panel-header" />
      <CardContent>
        {loading ? (
          <div>Loading...</div>
        ) : (
          <List dense disablePadding>
            {summaries.map(({ symbol, final_signal }) => {
              const chip = signalToChip(final_signal);
              return (
                <ListItemButton key={symbol} selected={symbol === selected} onClick={() => onSelect(symbol)} className="list-item-glow">
                  <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ width: '100%' }}>
                    <ListItemText primary={symbol} primaryTypographyProps={{ className: 'mono' }} />
                    <Chip label={chip.label} className={`chip-signal ${chip.className} hex-pulse-once`} size="small" />
                  </Stack>
                </ListItemButton>
              );
            })}
          </List>
        )}
      </CardContent>
    </Card>
  );
};

export default Dashboard;
