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


def check_alerts():
    try:
        alerts = load_alerts()
        triggered = []

        for alert in alerts:
            df = get_stock_data(alert["ticker"])

            if df is None or df.empty:
                continue

            price = float(df["Close"].iloc[-1])

            if price >= alert["target"]:
                triggered.append({
                    "ticker": alert["ticker"],
                    "target": alert["target"],
                    "current_price": price
                })

        return triggered

    except Exception as e:
        print("ALERT ERROR:", e)
        return []