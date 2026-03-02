import requests
import yagmail
from twilio.rest import Client

# ================= EMAIL =================
EMAIL = "sangeetass100@gmail.com"
EMAIL_PASS = "mdno pufx ymaw nhza"

def send_email_alert(to_email, subject, message):
    yag = yagmail.SMTP(EMAIL, EMAIL_PASS)
    yag.send(to_email, subject, message)

# ================= TELEGRAM =================
TELEGRAM_TOKEN = "8629893068:AAERHJNGMpcT0CZm3WplbRSjmSy-Ns-qYdQ"
CHAT_ID = "244514144"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

