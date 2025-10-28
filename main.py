import requests
from datetime import datetime

# ----- تنظیم آستانه ها -----
BUBBLE_UPPER_THRESHOLD = 20  # درصد حباب بالاتر از این مقدار → هشدار فروش
BUBBLE_LOWER_THRESHOLD = 12   # درصد حباب پایین‌تر از این مقدار → هشدار خرید

def fetch_data():
    url = "https://alanchand.com/media/api"  # endpoint JSON داده‌ها
    r = requests.get(url)
    data = r.json()
    
    gold_ounce_usd = float(data["gold_ounce"])
    usd_irr = float(data["usd"])
    coin_emami_market = float(data["coin_emami"])

    coin_intrinsic = gold_ounce_usd * 0.235 * usd_irr
    bubble_amount = coin_emami_market - coin_intrinsic
    bubble_percent = (bubble_amount / coin_intrinsic) * 100

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
    return result

if __name__ == "__main__":
    fetch_data()

    # بررسی آستانه‌ها
    if bubble_percent >= BUBBLE_UPPER_THRESHOLD:
        message = f"⚠️ هشدار: حباب سکه بالای {BUBBLE_UPPER_THRESHOLD}% است!\n{result}"
        send_telegram(message)
    elif bubble_percent <= BUBBLE_LOWER_THRESHOLD:
        message = f"⚠️ هشدار: حباب سکه پایین‌تر از {BUBBLE_LOWER_THRESHOLD}% است!\n{result}"
        send_telegram(message)

def send_telegram(message):
    BOT_TOKEN = "8118717249:AAFUzO_n97FWfHbIOcQQSRDuxWbDnPirrB4"
    CHAT_ID = "91349091"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("خطا در ارسال تلگرام:", e)
