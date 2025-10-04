import pandas as pd
import numpy as np
from backend.quantcode_analyzer import QuantCodeAnalyzer

class FakeAnalyzer(QuantCodeAnalyzer):
    def _fetch_data(self):
        # Build tiny deterministic dataset
        idx = pd.date_range('2024-01-01', periods=100, freq='D')
        # Create simple uptrend with a strong bullish divergence setup
        close = pd.Series(np.linspace(100, 150, 100), index=idx)
        open_ = close - 0.5
        high = close + 1.0
        low = close - 1.0
        vol = pd.Series(1000, index=idx)
        self.data = pd.DataFrame({'Open': open_, 'High': high, 'Low': low, 'Close': close, 'Volume': vol})
        self.latest_close_price = float(close.iloc[-1])
        return True


def test_confluence_score_and_signal_buy():
    a = FakeAnalyzer('TEST', days=60)
    res = a.get_final_signal()
    assert 'total_score' in res
    assert isinstance(res['total_score'], int)
    # Expect score threshold mapping to BUY/HOLD/SELL
    if res['total_score'] >= 3:
        assert res['final_signal'] == 'BUY'
    elif res['total_score'] <= -3:
        assert res['final_signal'] == 'SELL'
    else:
        assert res['final_signal'] == 'HOLD'
