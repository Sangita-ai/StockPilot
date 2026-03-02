import json
import os
from data_pipeline.stock_fetcher import get_stock_data


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "alerts.json")


if not os.path.exists(DB_PATH):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "w") as f:
        json.dump([], f)


def load_alerts():
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def save_alerts(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)


def add_alert(ticker, target):
    alerts = load_alerts()
    alerts.append({
        "ticker": ticker,
        "target": float(target)
    })
    save_alerts(alerts)


from ai_engine.alert_utils import send_telegram_alert

def check_alerts():
    triggered = []
    
    try:
        alerts = load_alerts()
        for alert in alerts:
            ticker = alert["ticker"]
            target = alert["target"]
            current_price = get_stock_data(ticker)
            
            if current_price >= target:
                message = f"{ticker} reached target {target}"
                send_email_alert("receiver@email.com", "Stock Alert", message)
                send_telegram_alert(message)
                triggered.append(alert)

        return triggered
    except Exception as e:
        print("ALERT ERROR:", e)
        return []