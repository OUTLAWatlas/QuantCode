import React, { useState } from 'react';
import { Card, CardHeader, CardContent, Typography, Chip, Divider, Box, Button } from '@mui/material';
import { TrendingUp, TrendingDown, PauseCircleOutline } from '@mui/icons-material';

const signalToChip = (signal) => {
  const s = (signal || '').toLowerCase();
  if (s === 'buy') return { label: 'BUY', className: 'chip-buy', icon: <TrendingUp className="icon-buy" /> };
  if (s === 'sell') return { label: 'SELL', className: 'chip-sell', icon: <TrendingDown className="icon-sell" /> };
  if (s === 'hold') return { label: 'HOLD', className: 'chip-hold', icon: <PauseCircleOutline className="icon-hold" /> };
  return { label: 'N/A', className: 'chip-neutral', icon: null };
};

const prettyName = (key) => key.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());

const AnalysisView = ({ analysisData }) => {
  // Toggle for showing/hiding the detailed breakdown
  const [showBreakdown, setShowBreakdown] = useState(true);

  if (!analysisData) return null;
  const final = (analysisData.final_signal || '').toUpperCase();
  const finalClass = final === 'BUY' ? 'neon-green' : final === 'SELL' ? 'neon-red' : 'chip-hold';

  const score = Number(analysisData?.total_score || 0);
  const scoreClass = score > 0 ? 'neon-green' : score < 0 ? 'neon-red' : 'chip-hold';
  const scoreText = score > 0 ? `+${score}` : `${score}`;

  const entries = Object.entries(analysisData?.analyses || {});

  return (
    <Card className="panel panel-frosted">
      <CardHeader title="Technical Analysis" subheader="Confluence" className="panel-header" />
      <CardContent>
        {/* Ticker and price (subtle) */}
        <Typography variant="h6" className="title-orbitron" gutterBottom>{analysisData.ticker}</Typography>
        {analysisData.latest_close_price != null && (
          <Typography variant="h5" gutterBottom className="mono">₹{Number(analysisData.latest_close_price || 0).toFixed(2)}</Typography>
        )}

        {/* Main Signal Display - prominent Orbitron, neon colored */}
        <div className="signal-banner hex-pulse-once" style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <Typography variant="h3" className={`title-orbitron ${finalClass}`}>
            {final}
          </Typography>
          {/* Small chip/icon accent */}
          {(() => { const chip = signalToChip(analysisData.final_signal); return (
            <Chip className={`chip-signal ${chip.className}`} label={chip.label} icon={chip.icon} />
          ); })()}
          <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>{analysisData.confidence}</Typography>
        </div>

        {/* Primary Trend & Confluence Score */}
        <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap', mb: 2, mt: 1 }}>
          <Typography variant="subtitle1" className="title-orbitron">
            Primary Trend: <span className="mono">{analysisData?.primary_trend?.trend || '—'}</span>
          </Typography>
          <Typography variant="subtitle1" className="title-orbitron">
            Confluence Score: <span className={`mono ${scoreClass}`}>{scoreText}</span>
          </Typography>
          <Button size="small" variant="outlined" className="btn-glow" onClick={() => setShowBreakdown(v => !v)}>
            {showBreakdown ? 'Hide Breakdown' : 'Show Breakdown'}
          </Button>
        </Box>

        <Divider sx={{ mb: 2, opacity: 0.3 }} />

        {/* Confluence Breakdown Grid with toggle */}
        {showBreakdown && (
          <>
            <Typography variant="h6" className="title-orbitron" gutterBottom>
              Confluence Breakdown
            </Typography>
            <div className="breakdown-grid breakdown-3cols">
              {entries.map(([key, analysis], idx) => {
                const chip = signalToChip(analysis?.signal);
                const s = Number(analysis?.score || 0);
                const sClass = s > 0 ? 'neon-green' : s < 0 ? 'neon-red' : 'chip-hold';
                const sText = s > 0 ? `+${s}` : `${s}`;
                return (
                  <div
                    key={key}
                    className="breakdown-item glitch-in"
                    style={{ animationDelay: `${idx * 60}ms` }}
                  >
                    <div className="breakdown-name mono">{prettyName(key)}</div>
                    <div className="breakdown-signal">
                      <Chip size="small" className={`chip-signal ${chip.className}`} label={chip.label} icon={chip.icon} />
                    </div>
                    <div className={`breakdown-score mono ${sClass}`}>{sText}</div>
                  </div>
                );
              })}
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default AnalysisView;
