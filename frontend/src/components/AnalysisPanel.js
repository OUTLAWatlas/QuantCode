import React from 'react';
import { Card, CardHeader, CardContent, Typography, Chip, Divider, Box } from '@mui/material';
import { TrendingUp, TrendingDown, PauseCircleOutline } from '@mui/icons-material';
import AnalysisBreakdown from './AnalysisBreakdown';

const signalToChip = (signal) => {
  const s = (signal || '').toLowerCase();
  if (s === 'buy') return { label: 'BUY', className: 'chip-buy', icon: <TrendingUp className="icon-buy" /> };
  if (s === 'sell') return { label: 'SELL', className: 'chip-sell', icon: <TrendingDown className="icon-sell" /> };
  if (s === 'hold') return { label: 'HOLD', className: 'chip-hold', icon: <PauseCircleOutline className="icon-hold" /> };
  return { label: 'N/A', className: 'chip-neutral', icon: null };
};

const AnalysisPanel = ({ results }) => {
  if (!results) return null;
  return (
    <Card className="panel panel-frosted">
      <CardHeader title="Technical Analysis" subheader="Breakdown" className="panel-header" />
      <CardContent>
        {results && (
          <>
            <Typography variant="h5" className="title-orbitron" gutterBottom>{results.ticker}</Typography>
            <Typography variant="h4" gutterBottom className="mono">₹{Number(results.latest_close_price || 0).toFixed(2)}</Typography>

            {/* Main Signal */}
            <div className="signal-banner hex-pulse-once">
              {(() => {
                const chip = signalToChip(results.final_signal);
                const neonClass = chip.label === 'BUY' ? 'neon-green' : chip.label === 'SELL' ? 'neon-red' : 'chip-hold';
                return (
                  <Chip className={`chip-signal ${chip.className} ${neonClass}`} label={chip.label} icon={chip.icon} />
                );
              })()}
              <Typography variant="body2" color="text.secondary" sx={{ ml: 2 }}>{results.confidence}</Typography>
            </div>

            {/* Primary Trend & Confluence Score */}
            <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap', mb: 2 }}>
              <Typography variant="subtitle1" className="title-orbitron">
                Primary Trend: <span className="mono">{results?.primary_trend?.trend || '—'}</span>
              </Typography>
              <Typography variant="subtitle1" className="title-orbitron">
                Confluence Score: {(() => {
                  const score = Number(results?.total_score || 0);
                  const cls = score > 0 ? 'neon-green' : score < 0 ? 'neon-red' : 'chip-hold';
                  return <span className={`mono ${cls}`}>{score > 0 ? `+${score}` : score}</span>;
                })()}
              </Typography>
            </Box>

            <Divider sx={{ mb: 2, opacity: 0.3 }} />

            {/* Breakdown Grid */}
            <AnalysisBreakdown analyses={results.analyses} />
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default AnalysisPanel;
