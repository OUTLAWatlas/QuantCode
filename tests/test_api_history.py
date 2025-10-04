import json
import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as c:
        yield c


def test_history_bad_days(client):
    rv = client.get('/api/history/AAPL?days=5')
    assert rv.status_code == 400


def test_history_ok_shape(client, monkeypatch):
    # Monkeypatch yf.download to avoid network
    import pandas as pd
    import numpy as np
    import types

    def fake_download(ticker, start=None, end=None, progress=False, auto_adjust=True, prepost=True, group_by='column'):
        idx = pd.date_range('2024-01-01', periods=10, freq='D')
        df = pd.DataFrame({
            'Open': np.linspace(100, 110, 10),
            'High': np.linspace(101, 111, 10),
            'Low':  np.linspace(99, 109, 10),
            'Close': np.linspace(100, 110, 10),
            'Volume': np.arange(10)*1000+1,
        }, index=idx)
        return df

    import yfinance as yf
    monkeypatch.setattr(yf, 'download', fake_download)

    rv = client.get('/api/history/TEST?days=30')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'series' in data and isinstance(data['series'], list)
    assert len(data['series']) == 10
    first = data['series'][0]
    assert 'time' in first and 'value' in first


def test_history_cache_hit(client, monkeypatch, caplog):
    # Ensure cache works by calling twice and expecting same payload quickly
    import pandas as pd
    import numpy as np

    calls = {'n': 0}
    def fake_download(ticker, start=None, end=None, progress=False, auto_adjust=True, prepost=True, group_by='column'):
        calls['n'] += 1
        idx = pd.date_range('2024-02-01', periods=5, freq='D')
        df = pd.DataFrame({
            'Open': np.linspace(10, 20, 5),
            'High': np.linspace(11, 21, 5),
            'Low':  np.linspace(9, 19, 5),
            'Close': np.linspace(10, 20, 5),
        }, index=idx)
        return df

    import yfinance as yf
    monkeypatch.setattr(yf, 'download', fake_download)

    # First call populates cache
    rv1 = client.get('/api/history/XYZ?days=30')
    assert rv1.status_code == 200

    # Second call should hit cache; fake_download shouldn't be called again
    rv2 = client.get('/api/history/XYZ?days=30')
    assert rv2.status_code == 200

    assert calls['n'] == 1
