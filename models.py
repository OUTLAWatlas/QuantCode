"""
Database models for the QuantCode Flask application.

This module defines the SQLAlchemy database instance (db) and ORM models
used throughout the backend. Designed for use with Flask-SQLAlchemy.

Usage (example):

    from flask import Flask
    from models import db

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quantcode.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

"""
from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# Flask-SQLAlchemy database object
# Initialize in your Flask app via: db.init_app(app)
db = SQLAlchemy()


# ---------------------------------------------------------------------------
# Ticker
# ---------------------------------------------------------------------------
class Ticker(db.Model):
    """User's watchlist of stock symbols.

    Columns:
      - id: Surrogate primary key
      - symbol: Ticker symbol (e.g., "AAPL", "RELIANCE.NS"). Unique and required.
    """

    __tablename__ = 'tickers'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(64), unique=True, nullable=False, index=True)

    def __repr__(self) -> str:  # pragma: no cover - debugging convenience
        return f"<Ticker id={self.id} symbol='{self.symbol}'>"


# ---------------------------------------------------------------------------
# AnalysisResult
# ---------------------------------------------------------------------------
class AnalysisResult(db.Model):
    """Historical record of analysis outputs for a ticker.

    Columns:
      - id: Surrogate primary key
      - ticker_symbol: The analyzed ticker symbol
      - timestamp: When the analysis was performed (defaults to now)
      - final_signal: Final confluence signal (e.g., BUY/SELL/HOLD)
      - total_score: Aggregate confluence score (integer)
      - primary_trend: High-level trend classification (e.g., Uptrend/Downtrend)
      - breakdown: JSON payload with per-indicator details
    """

    __tablename__ = 'analysis_results'

    id = db.Column(db.Integer, primary_key=True)
    ticker_symbol = db.Column(db.String(64), nullable=False, index=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    final_signal = db.Column(db.String(16), nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    primary_trend = db.Column(db.String(32), nullable=True)
    breakdown = db.Column(db.JSON, nullable=True)

    def __repr__(self) -> str:  # pragma: no cover - debugging convenience
        return (
            f"<AnalysisResult id={self.id} ticker='{self.ticker_symbol}' "
            f"ts={self.timestamp} signal='{self.final_signal}' score={self.total_score}>"
        )


# ---------------------------------------------------------------------------
# PaperTrade
# ---------------------------------------------------------------------------
class PaperTrade(db.Model):
    """Simulated trade log for tracking strategy performance.

    Columns:
      - id: Surrogate primary key
      - ticker_symbol: The traded ticker symbol
      - entry_timestamp: Time when the trade was opened
      - trade_type: Trade direction/type (e.g., 'LONG', 'SHORT')
      - entry_price: Entry price
      - stop_loss_price: Stop-loss price
      - status: 'OPEN' or 'CLOSED'
      - exit_price: Exit price when closed (nullable)
    """

    __tablename__ = 'paper_trades'

    id = db.Column(db.Integer, primary_key=True)
    ticker_symbol = db.Column(db.String(64), nullable=False, index=True)
    entry_timestamp = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    trade_type = db.Column(db.String(16), nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    stop_loss_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(8), nullable=False, default='OPEN', server_default='OPEN', index=True)
    exit_price = db.Column(db.Float, nullable=True)

    def __repr__(self) -> str:  # pragma: no cover - debugging convenience
        return (
            f"<PaperTrade id={self.id} ticker='{self.ticker_symbol}' type='{self.trade_type}' "
            f"status='{self.status}' entry={self.entry_price} exit={self.exit_price}>"
        )
