import schedule
import time
import os
from app import app
from models import db, Ticker, AnalysisResult
from backend.quantcode_analyzer import QuantCodeAnalyzer
from notifications import check_and_notify


def run_daily_analysis_job():
    with app.app_context():
        print("Running daily analysis job...")
        tickers = Ticker.query.all() if hasattr(Ticker, 'query') else db.session.query(Ticker).all()
        for ticker_obj in tickers:
            ticker_symbol = getattr(ticker_obj, 'symbol', None) or getattr(ticker_obj, 'ticker', None)
            if not ticker_symbol:
                continue
            try:
                analyzer = QuantCodeAnalyzer(ticker_symbol)
                result = analyzer.get_final_signal()
                # Save analysis result
                if not result.get('error'):
                    pt = result.get('primary_trend')
                    primary_trend_text = pt.get('trend') if isinstance(pt, dict) else (pt or None)
                    ar = AnalysisResult(
                        ticker_symbol=ticker_symbol,
                        final_signal=result.get('final_signal'),
                        total_score=int(result.get('total_score', 0)),
                        primary_trend=primary_trend_text,
                        breakdown=result.get('analyses', {})
                    )
                    db.session.add(ar)
                    db.session.commit()
                # Trigger notification if strong signal
                check_and_notify(ticker_symbol, result)
                print(f"Analyzed {ticker_symbol}: {result.get('final_signal')}")
            except Exception as e:
                print(f"Error analyzing {ticker_symbol}: {e}")


schedule.every().day.at("20:00").do(run_daily_analysis_job)

if __name__ == "__main__":
    print("QUANTCODE Scheduler started. Waiting for scheduled jobs...")
    while True:
        schedule.run_pending()
        time.sleep(1)
