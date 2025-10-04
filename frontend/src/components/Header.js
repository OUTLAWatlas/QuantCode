import React from 'react';
import { AppBar, Toolbar, Typography, Stack, Button } from '@mui/material';
import { ShowChart } from '@mui/icons-material';

const Header = ({ focusMode, onToggleFocus }) => {
  return (
    <AppBar position="sticky" color="transparent" enableColorOnDark className="singularity-appbar">
      <Toolbar>
        <Stack direction="row" alignItems="center" spacing={1} flex={1} className="glitch-in">
          <ShowChart sx={{ color: 'var(--sg-electric)', textShadow: '0 0 8px var(--sg-electric)' }} />
          <Typography variant="h5" className="title-orbitron neon-title">QUANTCODE</Typography>
          <Typography variant="body2" sx={{ ml: 2 }} color="text.secondary">Project Singularity</Typography>
        </Stack>
        <Button className="btn-glow" variant="outlined" onClick={onToggleFocus}>
          {focusMode ? 'Exit Focus' : 'Focus Mode'}
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
