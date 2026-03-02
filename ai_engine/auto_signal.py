from backend.main import analyze_stock
from ai_engine.alert_utils import send_telegram_alert

def auto_signal_bot(tickers):
    for t in tickers:
        result = analyze_stock(t)

        if result["signal"] == "Bullish":
            send_telegram_alert(f"{t} turned Bullish!")