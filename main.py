import requests
from datetime import datetime
import os

# ----- تنظیم آستانه‌ها -----
BUBBLE_UPPER_THRESHOLD = 19  # درصد حباب بالاتر از این مقدار → هشدار فروش
BUBBLE_LOWER_THRESHOLD = 12   # درصد حباب پایین‌تر از این مقدار → هشدار خرید

# دریافت توکن و chat_id از GitHub Secrets
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    """ارسال پیام به تلگرام"""
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ BOT_TOKEN یا CHAT_ID تعریف نشده‌اند.")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("خطا در ارسال تلگرام:", e)

def fetch_data():
    """دریافت داده‌ها و محاسبه حباب سکه امامی"""
    url = "https://alanchand.com/media/api"  # endpoint JSON داده‌ها
    try:
        r = requests.get(url)
        data = r.json()
    except Exception as e:
        print("خطا در دریافت داده‌ها:", e)
        return

    # داده‌ها
    gold_ounce_usd = float(data["gold_ounce"])
    usd_irr = float(d_
