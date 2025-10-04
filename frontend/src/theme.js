import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#0F3460',
      contrastText: '#FFFFFF',
    },
    background: {
      default: '#1A1A2E',
      paper: '#16213E',
    },
    success: {
      main: '#53BF9D',
    },
    error: {
      main: '#E94560',
    },
    text: {
      primary: '#FFFFFF',
      secondary: 'rgba(255,255,255,0.8)'
    },
  },
  typography: {
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
    h1: { fontFamily: "Poppins, 'Segoe UI', sans-serif", fontWeight: 600 },
    h2: { fontFamily: "Poppins, 'Segoe UI', sans-serif", fontWeight: 600 },
    h3: { fontFamily: "Poppins, 'Segoe UI', sans-serif", fontWeight: 600 },
    button: { textTransform: 'none', fontWeight: 600 },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      defaultProps: {
        variant: 'contained',
        disableElevation: true,
      },
      styleOverrides: {
        root: {
          boxShadow: '0 4px 8px rgba(0,0,0,0.3)',
          ':hover': {
            boxShadow: '0 8px 18px rgba(15,52,96,0.4)'
          }
        }
      }
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backdropFilter: 'blur(10px)',
          backgroundImage: 'none',
          boxShadow: '0 8px 24px rgba(0,0,0,0.35)'
        }
      }
    },
    MuiTextField: {
      defaultProps: {
        variant: 'filled',
        fullWidth: true,
      }
    }
  }
});

export default theme;
