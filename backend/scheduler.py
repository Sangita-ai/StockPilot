import time
try:
    import schedule
except ImportError:
    schedule = None
try:
    from ai_engine.alerts import check_alerts
except ImportError:
    check_alerts = None

def run_scheduler():
    schedule.every(2).minutes.do(check_alerts)

    while True:
        schedule.run_pending()
        time.sleep(1)