import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

const NeonGreen = '#39FF14';
const NeonRed = '#FF073A';
const NeonBg = '#181A20';
const NeonBorder = (signal) => signal === 'BUY' ? NeonGreen : NeonRed;

const labelStyle = {
  fontFamily: 'Orbitron, sans-serif',
  fontWeight: 'bold',
  letterSpacing: 1,
  color: '#00FFFF',
  fontSize: '1.1em',
};
const valueStyle = {
  fontFamily: 'Fira Code, monospace',
  color: '#fff',
  fontSize: '1.15em',
  background: 'rgba(57,255,20,0.07)',
  borderRadius: 4,
  padding: '2px 8px',
  marginLeft: 8,
};

export default function TradeSetupCard({ setup }) {
  if (!setup) return null;
  // Determine signal type by comparing entry/target
  const signal = setup.target_price > setup.entry_price ? 'BUY' : 'SELL';
  return (
    <Card
      elevation={8}
      sx={{
        background: NeonBg,
        border: `2.5px solid ${NeonBorder(signal)}`,
        boxShadow: `0 0 16px ${NeonBorder(signal)}`,
        mb: 3,
        mt: 2,
        borderRadius: 4,
        position: 'relative',
        overflow: 'visible',
      }}
      className="holo-panel"
    >
      <CardContent>
        <Typography variant="h5" sx={{ ...labelStyle, color: NeonBorder(signal), mb: 2 }}>
          Trade Setup Plan
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <span style={labelStyle}>Entry Price:</span>
            <span style={valueStyle}>₹{Number(setup.entry_price).toFixed(2)}</span>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <span style={labelStyle}>Stop-Loss:</span>
            <span style={valueStyle}>₹{Number(setup.stop_loss_price).toFixed(2)}</span>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <span style={labelStyle}>Target Price:</span>
            <span style={valueStyle}>₹{Number(setup.target_price).toFixed(2)}</span>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <span style={labelStyle}>Position Size:</span>
            <span style={valueStyle}>{setup.position_size}</span>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}
