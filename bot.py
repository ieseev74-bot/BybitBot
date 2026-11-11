import time
import requests
from pybit.unified_trading import HTTP

# --- ВСТАВЬТЕ СВОИ КЛЮЧИ ОТ BYBIT ВМЕСТО ТЕКСТА В КАВЫЧКАХ ---
API_KEY = "ВАШ_BYBIT_API_KEY"
API_SECRET = "ВАШ_BYBIT_API_SECRET"

# --- ВАШИ ДАННЫЕ TELEGRAM (Уже заполнены) ---
TELEGRAM_TOKEN = "9087625673:AAEpGVkh8ETeftNT8n88oIHqz2TV8bC1tRM"
TELEGRAM_CHAT_ID = "1727960394"

session = HTTP(
    testnet=True, # Тестовый режим Bybit
    api-key="z058TlYRtO47UZug4p"
    api_secret="jFikrFFCf4rRJqeFw5tsNxczNuBZOxO126dP"
)

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Ошибка Telegram: {e}")

def main():
    try:
        response = session.get_tickers(category="linear")
        tickers = response.get("result", {}).get("list", [])
        
        usdt_pairs = [t for t in tickers if t["symbol"].endswith("USDT")]
        usdt_pairs.sort(key=lambda x: abs(float(x.get("price24hPcnt", 0))), reverse=True)
        
        top_3 = [item["symbol"] for item in usdt_pairs[:3]]
        msg = f"🔍 *Аналіз ринку Bybit (Cloud)*\nТоп-3 волатильних монети зараз:\n" + "\n".join([f"• `{coin}`" for coin in top_3])
        
        send_telegram(msg)
        print("Повідомлення успішно надіслано в Telegram!")
    except Exception as e:
        print(f"Помилка при запиті до Bybit: {e}")

if __name__ == "__main__":
    main()
