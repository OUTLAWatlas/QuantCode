import React from 'react';
import { Card, CardHeader, CardContent, List, ListItemButton, ListItemText, Chip, Stack } from '@mui/material';

const signalToChip = (signal) => {
  const s = (signal || '').toLowerCase();
  if (s === 'buy') return { label: 'BUY', className: 'chip-buy' };
  if (s === 'sell') return { label: 'SELL', className: 'chip-sell' };
  if (s === 'hold') return { label: 'HOLD', className: 'chip-hold' };
  return { label: 'N/A', className: 'chip-neutral' };
};

const Dashboard = ({ tickers, summaries, loading, onSelect, selected }) => {
  return (
    <Card className="panel panel-frosted">
      <CardHeader title="Dashboard" subheader="Watchlist" className="panel-header" />
      <CardContent>
        <List dense disablePadding>
          {tickers.map(t => {
            const sig = summaries[t]?.final_signal;
            const chip = signalToChip(sig);
            return (
              <ListItemButton key={t} selected={t === selected} onClick={() => onSelect(t)} className="list-item-glow">
                <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ width: '100%' }}>
                  <ListItemText primary={t} primaryTypographyProps={{ className: 'mono' }} />
                  <Chip label={chip.label} className={`chip-signal ${chip.className} hex-pulse-once`} size="small" />
                </Stack>
              </ListItemButton>
            );
          })}
        </List>
      </CardContent>
    </Card>
  );
};

export default Dashboard;
