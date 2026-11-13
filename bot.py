import time
import requests
from pybit.unified_trading import HTTP

# --- ВСТАВЬТЕ СВОИ КЛЮЧИ ОТ BYBIT ВМЕСТО ТЕКСТА В КАВЫЧКАХ ---
API_KEY = "z058TlYRtO47UZug4p"
API_SECRET = "jFikrFFCf4rRJqeFw5tsNxczNuBZOxO126dP"

# --- ВАШИ ДАННЫЕ TELEGRAM (Уже заполнены) ---
TELEGRAM_TOKEN = "9087652673:AAepGVKh8ETefnT8n8oIhqQzT"
TELEGRAM_CHAT_ID = "1727960394"

session = HTTP(
    testnet=True, # Тестовый режим Bybit
    api_key=API_KEY,
    api_secret=API_SECRET
)

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Ошибка Telegram: {e}")

def main():
    try:
        response = session.get_tickers(category="linear")
        tickers = response.get("result", {}).get("list", [])

        usdt_pairs = [t for t in tickers if t["symbol"].endswith("USDT")]
        usdt_pairs.sort(key=lambda x: float(x["turnover24h"]), reverse=True)

        top_3 = [item["symbol"] for item in usdt_pairs[:3]]
        message = "🔥 Аналіз ринку Bybit (USDT):\n" + "\n".join(f"- {s}" for s in top_3)
        
        send_telegram(message)
    except Exception as e:
        print(f"Помилка: {e}")

main()
