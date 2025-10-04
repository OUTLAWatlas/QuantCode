"""
Notification utilities for QUANTCODE
====================================

This module provides:
  - send_email_notification(subject, body): Sends an email via Gmail SMTP using
    credentials stored in environment variables.
  - check_and_notify(ticker, latest_analysis_result): Checks the final signal and
    sends an alert if it's a BUY/SELL and hasn't already been sent today for the
    same ticker and signal.

Environment variables used:
  - QUANTCODE_EMAIL_FROM: Gmail address to send from (required)
  - QUANTCODE_EMAIL_PASSWORD: Gmail App Password (required)
  - QUANTCODE_EMAIL_TO: Comma-separated recipient list (optional; defaults to FROM)
  - QUANTCODE_ALERTS_DB: Optional path to a JSON file storing sent-alert state

Notes:
  - For Gmail, you should use an App Password with 2FA enabled
    https://support.google.com/accounts/answer/185833
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, date
from email.message import EmailMessage
import smtplib
from typing import Dict, Optional, List, Tuple

logger = logging.getLogger(__name__)


def _state_file_path() -> str:
    """Resolve the alerts state file path."""
    custom = os.getenv("QUANTCODE_ALERTS_DB")
    if custom:
        return custom
    # Store alongside this module by default
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, ".alert_state.json")


def _load_state() -> Dict[str, Dict[str, str]]:
    """Load the sent alerts state JSON. Structure:
    {
      "2025-10-05": {
        "RELIANCE.NS|BUY": "2025-10-05T09:34:00"
      }
    }
    """
    path = _state_file_path()
    try:
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning("Failed to load alert state (%s): %s", path, e)
        return {}


def _save_state(state: Dict[str, Dict[str, str]]) -> None:
    path = _state_file_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error("Failed to save alert state (%s): %s", path, e)


def send_email_notification(subject: str, body: str, *, to_addresses: Optional[List[str]] = None) -> bool:
    """Send an email using Gmail SMTP.

    Environment:
      - QUANTCODE_EMAIL_FROM
      - QUANTCODE_EMAIL_PASSWORD
      - QUANTCODE_EMAIL_TO (optional)

    Returns True on success, False on failure.
    """
    from_addr = os.getenv("QUANTCODE_EMAIL_FROM")
    password = os.getenv("QUANTCODE_EMAIL_PASSWORD")
    env_to = os.getenv("QUANTCODE_EMAIL_TO")

    if not from_addr or not password:
        logger.warning("Email not sent: QUANTCODE_EMAIL_FROM or QUANTCODE_EMAIL_PASSWORD is not set")
        return False

    if to_addresses is None:
        if env_to:
            to_addresses = [addr.strip() for addr in env_to.split(",") if addr.strip()]
        else:
            to_addresses = [from_addr]

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addresses)
    msg.set_content(body)

    try:
        # Gmail SMTP over SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_addr, password)
            smtp.send_message(msg)
        logger.info("Email sent to %s: %s", msg["To"], subject)
        return True
    except Exception as e:
        logger.error("Email send failed: %s", e)
        return False


def _format_subject_body(ticker: str, result: Dict) -> Tuple[str, str]:
    """Create a professional subject and body for the alert."""
    final_signal = str(result.get("final_signal", "")).upper()
    total_score = result.get("total_score", 0)
    trend = (result.get("primary_trend") or {}).get("trend", "—")
    price = result.get("latest_close_price")
    when = datetime.now().strftime("%Y-%m-%d %H:%M")

    subject = f"QUANTCODE Signal Alert: {final_signal} signal for {ticker}"

    lines = [
        f"QUANTCODE Trading Signal",
        f"Timestamp: {when}",
        "",
        f"Ticker: {ticker}",
        f"Final Signal: {final_signal}",
        f"Confluence Score: {total_score}",
        f"Primary Trend: {trend}",
    ]
    if price is not None:
        try:
            lines.append(f"Latest Close: {float(price):.2f}")
        except Exception:
            lines.append(f"Latest Close: {price}")

    analyses = result.get("analyses") or {}
    if analyses:
        lines.extend(["", "Breakdown:"])
        for key, a in analyses.items():
            sig = a.get("signal", "—")
            sc = a.get("score", 0)
            key_pretty = key.replace("_", " ").title()
            lines.append(f"  - {key_pretty}: {sig} (score {sc})")

    lines.extend(["", "—", "Automated alert from QUANTCODE"]) 
    body = "\n".join(lines)
    return subject, body


def check_and_notify(ticker: str, latest_analysis_result: Dict) -> bool:
    """Check the analysis result and send an email alert if needed.

    Rules:
      - Only alerts for BUY or SELL final_signal.
      - Prevent duplicate alerts for the same ticker and same signal on the same day.

    Returns True if an alert was sent, False otherwise (including duplicates).
    """
    if not latest_analysis_result:
        return False

    final_signal = str(latest_analysis_result.get("final_signal", "")).upper()
    if final_signal not in {"BUY", "SELL"}:
        return False

    today = date.today().strftime("%Y-%m-%d")
    key = f"{ticker}|{final_signal}"

    state = _load_state()
    day_map = state.get(today, {})

    if key in day_map:
        # Already sent this signal for this ticker today
        logger.info("Duplicate alert suppressed for %s on %s (%s)", ticker, today, final_signal)
        return False

    # Create email content and send
    subject, body = _format_subject_body(ticker, latest_analysis_result)
    sent = send_email_notification(subject, body)

    if sent:
        # Record state and persist
        day_map[key] = datetime.now().isoformat(timespec="seconds")
        state[today] = day_map
        _save_state(state)
        return True

    return False


__all__ = [
    "send_email_notification",
    "check_and_notify",
]
