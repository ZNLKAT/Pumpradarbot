import requests
import time
from telegram import Bot

# === KONFIGURATION ===
BOT_TOKEN = 'DEIN_BOT_TOKEN_HIER'
CHAT_ID = DEINE_CHAT_ID_HIER
CHECK_INTERVAL = 60  # Sekunden

bot = Bot(token=BOT_TOKEN)
last_data = {}

# KuCoin-Daten abrufen
def get_tickers():
    url = "https://api.kucoin.com/api/v1/market/allTickers"
    response = requests.get(url)
    return response.json()["data"]["ticker"]

# Frühe Gainer erkennen
def scan_for_early_gainers(tickers):
    for coin in tickers:
        symbol = coin['symbol']
        if not symbol.endswith("USDT"):
            continue

        try:
            price = float(coin['last'])
            vol = float(coin['volValue'])
        except:
            continue

        if symbol in last_data:
            old_price = last_data[symbol]['price']
            old_vol = last_data[symbol]['vol']
            price_change = ((price - old_price) / old_price) * 100
            vol_change = ((vol - old_vol) / old_vol) * 100

            if 0.5 <= price_change <= 1.5 and vol_change >= 10:
                message = f"⚠️ Frühwarnung: {symbol}\nPreis: {price:.6f} USDT\n+{price_change:.2f}% | Volumen +{vol_change:.2f}%"
                bot.send_message(chat_id=CHAT_ID, text=message)

        last_data[symbol] = {'price': price, 'vol': vol}

# Hauptloop
def main():
    while True:
        try:
            tickers = get_tickers()
            scan_for_early_gainers(tickers)
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            bot.send_message(chat_id=CHAT_ID, text=f"❌ Fehler: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
    Fix: Bot Code aktualisiert
    
