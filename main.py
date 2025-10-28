import requests
from datetime import datetime
import os

# ----- تنظیم آستانه‌ها -----
BUBBLE_UPPER_THRESHOLD = 12  # درصد حباب بالاتر از این مقدار → هشدار فروش
BUBBLE_LOWER_THRESHOLD = 5   # درصد حباب پایین‌تر از این مقدار → هشدار خرید

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
    usd_irr = float(data["usd"])
    coin_emami_market = float(data["coin_emami"])

    # محاسبه قیمت ذاتی سکه
    coin_intrinsic = gold_ounce_usd * 0.235 * usd_irr

    # میزان و درصد حباب
    bubble_amount = coin_emami_market - coin_intrinsic
    bubble_percent = (bubble_amount / coin_intrinsic) * 100

    # خروجی
    result = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "gold_ounce_usd": gold_ounce_usd,
        "usd_irr": usd_irr,
        "coin_emami_market": coin_emami_market,
        "coin_emami_intrinsic": int(coin_intrinsic),
        "bubble_percent": round(bubble_percent, 2),
        "bubble_amount": int(bubble_amount)
    }

    print(result)

    # بررسی آستانه‌ها و ارسال هشدار تلگرام
    if bubble_percent >= BUBBLE_UPPER_THRESHOLD:
        message = f"⚠️ هشدار: حباب سکه بالای {BUBBLE_UPPER_THRESHOLD}% است!\n{result}"
        send_telegram(message)
    elif bubble_percent <= BUBBLE_LOWER_THRESHOLD:
        message = f"⚠️ هشدار: حباب سکه پایین‌تر از {BUBBLE_LOWER_THRESHOLD}% است!\n{result}"
        send_telegram(message)

    return result

if __name__ == "__main__":
    fetch_data()
