import React from 'react';
import { Card, CardHeader, CardContent, Chip, Typography } from '@mui/material';
import { TrendingUp, TrendingDown, PauseCircleOutline } from '@mui/icons-material';

const signalToChip = (signal) => {
  const s = (signal || '').toLowerCase();
  if (s === 'buy') return { label: 'BUY', className: 'chip-buy', icon: <TrendingUp className="icon-buy" /> };
  if (s === 'sell') return { label: 'SELL', className: 'chip-sell', icon: <TrendingDown className="icon-sell" /> };
  if (s === 'hold') return { label: 'HOLD', className: 'chip-hold', icon: <PauseCircleOutline className="icon-hold" /> };
  return { label: 'N/A', className: 'chip-neutral', icon: null };
};

const prettyName = (key) => key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

const AnalysisBreakdown = ({ analyses }) => {
  const entries = Object.entries(analyses || {});
  if (!entries.length) return null;

  return (
    <div className="breakdown-section">
      <Typography variant="h6" className="title-orbitron" gutterBottom>
        Signal Confluence Breakdown
      </Typography>
      <div className="breakdown-grid">
        {entries.map(([key, analysis], idx) => {
          const chip = signalToChip(analysis?.signal);
          const score = Number(analysis?.score || 0);
          const scoreClass = score > 0 ? 'neon-green' : score < 0 ? 'neon-red' : 'chip-hold';
          const scoreText = score > 0 ? `+${score}` : `${score}`;
          return (
            <div className="breakdown-item fade-in-up" style={{ animationDelay: `${idx * 70}ms` }} key={key}>
              <Card className="mini-panel">
                <CardHeader
                  title={prettyName(key)}
                  titleTypographyProps={{ className: 'title-orbitron' }}
                  action={<Chip label={chip.label} className={`chip-signal ${chip.className}`} size="small" icon={chip.icon} />}
                />
                <CardContent>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {analysis?.details || '—'}
                  </Typography>
                  <Typography variant="subtitle2" className={`mono ${scoreClass}`}>
                    Score: {scoreText}
                  </Typography>
                </CardContent>
              </Card>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AnalysisBreakdown;
