import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/design-system.css';
import './styles/singularity.css';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme';

/**
 * Entry point for the QuantCode React application
 * Renders the main App component into the DOM
 */

// Create root element and render app
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>
);