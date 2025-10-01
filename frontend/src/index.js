import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

/**
 * Entry point for the QuantCode React application
 * Renders the main App component into the DOM
 */

// Create root element and render app
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);