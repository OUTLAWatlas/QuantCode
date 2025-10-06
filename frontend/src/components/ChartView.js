import React, { useEffect, useRef, useState } from 'react';
import { Card, CardHeader, CardContent, Stack, Button, ButtonGroup } from '@mui/material';

// Helper to create chart with Project Singularity theme
const createThemedChart = (lwcModule, container, width, height) =>
  lwcModule.createChart(container, {
    width,
    height,
    layout: { background: { type: 'solid', color: '#0D0D2B' }, textColor: '#F8F8FF', fontFamily: 'Fira Code, monospace' },
    grid: { vertLines: { color: 'rgba(255,255,255,0.06)' }, horzLines: { color: 'rgba(255,255,255,0.06)' } },
    rightPriceScale: { borderColor: 'rgba(255,255,255,0.1)' },
    timeScale: { borderColor: 'rgba(255,255,255,0.1)' },
    crosshair: { mode: 1 },
    localization: { priceFormatter: (p) => `₹${p.toFixed(2)}` },
    watermark: { visible: false },
  });

const ChartView = ({ ticker, chartData }) => {
  // Load lightweight-charts dynamically to avoid ESM/CJS interop issues
  const [lwc, setLwc] = useState(null);
  const lwcSetRef = useRef(false);
  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const mod = await import('lightweight-charts');
        const createChart = mod.createChart || (mod.default && mod.default.createChart);
        const LineStyle = mod.LineStyle || (mod.default && mod.default.LineStyle);
        const LineSeries = mod.LineSeries || (mod.default && mod.default.LineSeries);
        const HistogramSeries = mod.HistogramSeries || (mod.default && mod.default.HistogramSeries);
        if (mounted && createChart) { setLwc({ createChart, LineStyle, LineSeries, HistogramSeries }); lwcSetRef.current = true; }
      } catch (e) {
        // eslint-disable-next-line no-console
        console.error('Failed to load lightweight-charts', e);
      }
      // Fallback to window.LightweightCharts if available (e.g., loaded via script tag)
      if (mounted && typeof window !== 'undefined' && window.LightweightCharts && !lwcSetRef.current) {
        const createChart = window.LightweightCharts.createChart;
        const LineStyle = window.LightweightCharts.LineStyle;
        const LineSeries = window.LightweightCharts.LineSeries;
        const HistogramSeries = window.LightweightCharts.HistogramSeries;
        if (createChart) { setLwc({ createChart, LineStyle, LineSeries, HistogramSeries }); lwcSetRef.current = true; }
      }
    })();
    return () => { mounted = false; };
  }, []);
  // Container refs for panes
  const priceContainerRef = useRef(null);
  const rsiContainerRef = useRef(null);
  const macdContainerRef = useRef(null);

  // Chart refs and series refs
  const priceChartRef = useRef(null);
  const rsiChartRef = useRef(null);
  const macdChartRef = useRef(null);

  const priceSeriesRef = useRef(null);
  const ema20Ref = useRef(null);
  const ema50Ref = useRef(null);
  const bbUpperRef = useRef(null);
  const bbMiddleRef = useRef(null);
  const bbLowerRef = useRef(null);
  const rsiSeriesRef = useRef(null);
  const macdLineRef = useRef(null);
  const macdSignalRef = useRef(null);
  const macdHistRef = useRef(null);
  const rsiOverboughtLineRef = useRef(null);
  const rsiOversoldLineRef = useRef(null);
  const macdZeroLineRef = useRef(null);

  // Data maps for crosshair sync
  const priceMapRef = useRef(new Map());
  const rsiMapRef = useRef(new Map());
  const macdMapRef = useRef(new Map());

  // Toggles
  const [showEMA, setShowEMA] = useState(true);
  const [showBB, setShowBB] = useState(true);
  const [showRSI, setShowRSI] = useState(true);
  const [showMACD, setShowMACD] = useState(true);

  // Sizes
  const baseHeight = 360;
  const rsiHeight = 120;
  const macdHeight = 160;

  // Create/destroy Price chart once
  useEffect(() => {
    if (!lwc?.createChart) return;
    const container = priceContainerRef.current;
    if (!container) return;
    // Create once
    if (priceChartRef.current) return;
  const width = container.clientWidth || 600;
  const priceChart = createThemedChart(lwc, container, width, baseHeight);
    priceChartRef.current = priceChart;
    // Main price series
    if (typeof priceChart.addSeries !== 'function') {
      // eslint-disable-next-line no-console
      console.error('Chart API missing addSeries (v5 API). Chart object:', priceChart);
      return () => { try { priceChart.remove && priceChart.remove(); } catch {} };
    }
    if (lwc.LineSeries) {
      priceSeriesRef.current = priceChart.addSeries(lwc.LineSeries, { color: '#00BFFF', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
    } else if (typeof priceChart.addLineSeries === 'function') {
      priceSeriesRef.current = priceChart.addLineSeries({ color: '#00BFFF', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
    }
    // Overlays
    if (lwc.LineSeries) {
      bbUpperRef.current = priceChart.addSeries(lwc.LineSeries, { color: 'rgba(173,216,230,0.8)', lineWidth: 1, lastValueVisible: true, priceLineVisible: false });
      bbMiddleRef.current = priceChart.addSeries(lwc.LineSeries, { color: 'rgba(255,255,255,0.6)', lineWidth: 1, lineStyle: 1, lastValueVisible: true, priceLineVisible: false });
      bbLowerRef.current = priceChart.addSeries(lwc.LineSeries, { color: 'rgba(173,216,230,0.8)', lineWidth: 1, lastValueVisible: true, priceLineVisible: false });
    } else {
      bbUpperRef.current = priceChart.addLineSeries({ color: 'rgba(173,216,230,0.8)', lineWidth: 1, lastValueVisible: true, priceLineVisible: false });
      bbMiddleRef.current = priceChart.addLineSeries({ color: 'rgba(255,255,255,0.6)', lineWidth: 1, lineStyle: 1, lastValueVisible: true, priceLineVisible: false });
      bbLowerRef.current = priceChart.addLineSeries({ color: 'rgba(173,216,230,0.8)', lineWidth: 1, lastValueVisible: true, priceLineVisible: false });
    }

    const onResize = () => {
      const w = container.clientWidth || width;
      priceChart.applyOptions({ width: w, height: baseHeight });
    };
    window.addEventListener('resize', onResize);
    return () => {
      window.removeEventListener('resize', onResize);
      try { priceChart.remove(); } catch {}
      priceChartRef.current = null;
      priceSeriesRef.current = null;
      ema20Ref.current = null;
      ema50Ref.current = null;
      bbUpperRef.current = null;
      bbMiddleRef.current = null;
      bbLowerRef.current = null;
    };
  }, [lwc]);

  // Create/destroy RSI chart based on toggle
  useEffect(() => {
    if (!lwc?.createChart) return;
    const container = rsiContainerRef.current;
    if (!container) return;
    if (!showRSI) {
      // destroy existing
      if (rsiChartRef.current) { try { rsiChartRef.current.remove(); } catch {} rsiChartRef.current = null; }
      rsiSeriesRef.current = null;
      return;
    }
  const width = container.clientWidth || (priceContainerRef.current?.clientWidth || 600);
  const rsiChart = createThemedChart(lwc, container, width, rsiHeight);
    rsiChartRef.current = rsiChart;
    if (typeof rsiChart.addSeries !== 'function') {
      // eslint-disable-next-line no-console
      console.error('RSI chart missing addSeries (v5 API). Chart object:', rsiChart);
      return () => { try { rsiChart.remove && rsiChart.remove(); } catch {} };
    }
    if (lwc.LineSeries) {
      rsiSeriesRef.current = rsiChart.addSeries(lwc.LineSeries, { color: '#7CFC00', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
    } else {
      rsiSeriesRef.current = rsiChart.addLineSeries({ color: '#7CFC00', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
    }
    // RSI guide lines (30/70) with dashed neon styles
    try {
      rsiOverboughtLineRef.current = rsiSeriesRef.current.createPriceLine({
        price: 70,
        color: 'rgba(255, 71, 87, 0.65)', // Neon Red semi-transparent
        lineStyle: lwc.LineStyle?.Dashed ?? 1,
        lineWidth: 1,
        axisLabelVisible: true,
        title: 'Overbought',
      });
      rsiOversoldLineRef.current = rsiSeriesRef.current.createPriceLine({
        price: 30,
        color: 'rgba(0, 255, 136, 0.65)', // Neon Green semi-transparent
        lineStyle: lwc.LineStyle?.Dashed ?? 1,
        lineWidth: 1,
        axisLabelVisible: true,
        title: 'Oversold',
      });
    } catch {}
    const onResize = () => {
      const w = container.clientWidth || width;
      rsiChart.applyOptions({ width: w, height: rsiHeight });
    };
    window.addEventListener('resize', onResize);
    return () => {
      window.removeEventListener('resize', onResize);
      if (rsiChartRef.current) { try { rsiChartRef.current.remove(); } catch {} rsiChartRef.current = null; }
      rsiSeriesRef.current = null;
      rsiOverboughtLineRef.current = null;
      rsiOversoldLineRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [showRSI, lwc]);

  // Create/destroy MACD chart based on toggle
  useEffect(() => {
    if (!lwc?.createChart) return;
    const container = macdContainerRef.current;
    if (!container) return;
    if (!showMACD) {
      if (macdChartRef.current) { try { macdChartRef.current.remove(); } catch {} macdChartRef.current = null; }
      macdLineRef.current = null;
      macdSignalRef.current = null;
      macdHistRef.current = null;
      return;
    }
  const width = container.clientWidth || (priceContainerRef.current?.clientWidth || 600);
  const macdChart = createThemedChart(lwc, container, width, macdHeight);
    macdChartRef.current = macdChart;
    if (typeof macdChart.addSeries !== 'function') {
      // eslint-disable-next-line no-console
      console.error('MACD chart missing addSeries (v5 API). Chart object:', macdChart);
      return () => { try { macdChart.remove && macdChart.remove(); } catch {} };
    }
    if (lwc.LineSeries) {
      macdLineRef.current = macdChart.addSeries(lwc.LineSeries, { color: '#1E90FF', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
      macdSignalRef.current = macdChart.addSeries(lwc.LineSeries, { color: '#FF4500', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
    } else {
      macdLineRef.current = macdChart.addLineSeries({ color: '#1E90FF', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
      macdSignalRef.current = macdChart.addLineSeries({ color: '#FF4500', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
    }
    if (lwc.HistogramSeries) {
      macdHistRef.current = macdChart.addSeries(lwc.HistogramSeries, { base: 0, priceFormat: { type: 'price', precision: 2, minMove: 0.01 }, lastValueVisible: true });
    } else if (typeof macdChart.addHistogramSeries === 'function') {
      macdHistRef.current = macdChart.addHistogramSeries({ base: 0, priceFormat: { type: 'price', precision: 2, minMove: 0.01 }, lastValueVisible: true });
    } else {
      // eslint-disable-next-line no-console
      console.warn('Histogram series not available on MACD chart; skipping histogram.');
    }
    // MACD zero line (dashed ghost white)
    try {
      macdZeroLineRef.current = macdLineRef.current.createPriceLine({
        price: 0,
        color: 'rgba(248, 248, 255, 0.65)', // Ghost White semi-transparent
        lineStyle: lwc.LineStyle?.Dashed ?? 1,
        lineWidth: 1,
        axisLabelVisible: true,
        title: 'Zero',
      });
    } catch {}
    const onResize = () => {
      const w = container.clientWidth || width;
      macdChart.applyOptions({ width: w, height: macdHeight });
    };
    window.addEventListener('resize', onResize);
    return () => {
      window.removeEventListener('resize', onResize);
      if (macdChartRef.current) { try { macdChartRef.current.remove(); } catch {} macdChartRef.current = null; }
      macdLineRef.current = null;
      macdSignalRef.current = null;
      macdHistRef.current = null;
      macdZeroLineRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [showMACD, lwc]);

  // Set data into series when chartData changes
  useEffect(() => {
    const cd = chartData || {};
    // Price and overlays
    if (priceSeriesRef.current && Array.isArray(cd.close)) {
      priceSeriesRef.current.setData(cd.close);
      // Build time->price map
      priceMapRef.current.clear();
      cd.close.forEach(pt => { priceMapRef.current.set(pt.time, pt.value); });
      try { priceChartRef.current?.timeScale().fitContent(); } catch {}
    }
  // EMA handled by its own toggle effect
    if (bbUpperRef.current) bbUpperRef.current.setData(showBB && Array.isArray(cd.bollinger_upper) ? cd.bollinger_upper : []);
    if (bbMiddleRef.current) bbMiddleRef.current.setData(showBB && Array.isArray(cd.bollinger_middle) ? cd.bollinger_middle : []);
    if (bbLowerRef.current) bbLowerRef.current.setData(showBB && Array.isArray(cd.bollinger_lower) ? cd.bollinger_lower : []);

    // RSI
    if (rsiSeriesRef.current && Array.isArray(cd.rsi14)) {
      rsiSeriesRef.current.setData(cd.rsi14);
      rsiMapRef.current.clear();
      cd.rsi14.forEach(pt => { rsiMapRef.current.set(pt.time, pt.value); });
      try { rsiChartRef.current?.timeScale().fitContent(); } catch {}
    }

    // MACD
    if (macdLineRef.current && Array.isArray(cd.macd)) {
      macdLineRef.current.setData(cd.macd);
      macdMapRef.current.clear();
      cd.macd.forEach(pt => { macdMapRef.current.set(pt.time, pt.value); });
    }
    if (macdSignalRef.current && Array.isArray(cd.macd_signal)) {
      macdSignalRef.current.setData(cd.macd_signal);
    }
    if (macdHistRef.current && Array.isArray(cd.macd_histogram)) {
      // Color histogram bars by sign
      const hist = cd.macd_histogram.map(pt => ({ ...pt, color: (pt.value >= 0 ? 'rgba(0,200,5,0.8)' : 'rgba(220,0,0,0.8)') }));
      macdHistRef.current.setData(hist);
      try { macdChartRef.current?.timeScale().fitContent(); } catch {}
    }
  }, [chartData, showEMA, showBB]);

  // EMA toggle and data handling (create/remove on toggle)
  useEffect(() => {
    const priceChart = priceChartRef.current;
    if (!priceChart) return;
    const cd = chartData || {};
    if (showEMA) {
      // Create series if missing
      if (!ema20Ref.current) {
        if (lwc?.LineSeries && priceChart.addSeries) {
          ema20Ref.current = priceChart.addSeries(lwc.LineSeries, { color: '#FFD700', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
        } else if (typeof priceChart.addLineSeries === 'function') {
          ema20Ref.current = priceChart.addLineSeries({ color: '#FFD700', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
        }
      }
      if (!ema50Ref.current) {
        if (lwc?.LineSeries && priceChart.addSeries) {
          ema50Ref.current = priceChart.addSeries(lwc.LineSeries, { color: '#FF8C00', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
        } else if (typeof priceChart.addLineSeries === 'function') {
          ema50Ref.current = priceChart.addLineSeries({ color: '#FF8C00', lineWidth: 2, lastValueVisible: true, priceLineVisible: false });
        }
      }
      // Set data
      if (ema20Ref.current) ema20Ref.current.setData(Array.isArray(cd.ema20) ? cd.ema20 : []);
      if (ema50Ref.current) ema50Ref.current.setData(Array.isArray(cd.ema50) ? cd.ema50 : []);
    } else {
      // Remove series if exist
      if (ema20Ref.current) { try { priceChart.removeSeries(ema20Ref.current); } catch {} ema20Ref.current = null; }
      if (ema50Ref.current) { try { priceChart.removeSeries(ema50Ref.current); } catch {} ema50Ref.current = null; }
    }
  }, [showEMA, chartData, lwc]);

  // Synchronize time scales and crosshair between charts
  useEffect(() => {
    const priceChart = priceChartRef.current;
    const rsiChart = rsiChartRef.current;
    const macdChart = macdChartRef.current;
    const charts = [priceChart, showRSI ? rsiChart : null, showMACD ? macdChart : null].filter(Boolean);
    if (charts.length <= 1) return;

    let syncingRange = false;
    const handlers = [];
    charts.forEach((chart, idx) => {
      const h = chart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
        if (syncingRange || !range) return;
        syncingRange = true;
        charts.forEach((other, j) => { if (j !== idx) { try { other.timeScale().setVisibleLogicalRange(range); } catch {} } });
        syncingRange = false;
      });
      handlers.push({ chart, type: 'range', h });
    });

    // Crosshair sync
    let syncingCrosshair = false;
    const crosshairHandlers = [];
    const setCrosshair = (chart, price, time) => {
      try { chart.setCrosshairPosition && chart.setCrosshairPosition(price, time); } catch {}
    };
    const clearCrosshair = (chart) => {
      try { chart.clearCrosshairPosition && chart.clearCrosshairPosition(); } catch {}
    };
    charts.forEach((chart, idx) => {
      const h = chart.subscribeCrosshairMove(param => {
        if (syncingCrosshair) return;
        syncingCrosshair = true;
        const t = param?.time;
        if (!t) {
          charts.forEach((other, j) => { if (j !== idx) clearCrosshair(other); });
          syncingCrosshair = false; return;
        }
        // Pick values from maps to position crosshair meaningfully
        const priceVal = priceMapRef.current.get(t);
        const rsiVal = rsiMapRef.current.get(t);
        const macdVal = macdMapRef.current.get(t);
        charts.forEach((other, j) => {
          if (j === idx) return;
          if (other === priceChart && priceVal != null) setCrosshair(other, priceVal, t);
          else if (other === rsiChart && rsiVal != null) setCrosshair(other, rsiVal, t);
          else if (other === macdChart && macdVal != null) setCrosshair(other, macdVal, t);
        });
        syncingCrosshair = false;
      });
      crosshairHandlers.push({ chart, type: 'crosshair', h });
    });

    return () => {
      // There is no unsubscribe returned by lightweight-charts; but we can safely drop refs on cleanup
      // and charts will be removed in their own effects.
    };
  }, [showRSI, showMACD]);

  return (
    <Card className="panel panel-frosted">
      <CardHeader
        title={`Chart — ${ticker || '—'}`}
        subheader={"Price • RSI • MACD (synchronized)"}
        className="panel-header"
        action={
          <Stack direction="row" spacing={1} alignItems="center">
            <ButtonGroup size="small" variant="outlined" sx={{ mr: 1 }}>
              <Button onClick={() => setShowEMA(v => !v)} className="btn-glow" color={showEMA ? 'success' : 'inherit'}>
                EMA
              </Button>
              <Button onClick={() => setShowBB(v => !v)} className="btn-glow" color={showBB ? 'success' : 'inherit'}>
                BB
              </Button>
            </ButtonGroup>
            <ButtonGroup size="small" variant="outlined">
              <Button onClick={() => setShowRSI(v => !v)} className="btn-glow" color={showRSI ? 'success' : 'inherit'}>
                {showRSI ? 'Hide RSI' : 'Show RSI'}
              </Button>
              <Button onClick={() => setShowMACD(v => !v)} className="btn-glow" color={showMACD ? 'success' : 'inherit'}>
                {showMACD ? 'Hide MACD' : 'Show MACD'}
              </Button>
            </ButtonGroup>
          </Stack>
        }
      />
      <CardContent>
        <div className="glitch-in" style={{ width: '100%' }}>
          {/* Price pane */}
          <div ref={priceContainerRef} style={{ width: '100%', height: baseHeight }} />
          {/* RSI pane */}
          {showRSI && <div ref={rsiContainerRef} style={{ width: '100%', height: rsiHeight, marginTop: 8 }} />}
          {/* MACD pane */}
          {showMACD && <div ref={macdContainerRef} style={{ width: '100%', height: macdHeight, marginTop: 8 }} />}
        </div>
      </CardContent>
    </Card>
  );
};

export default ChartView;
