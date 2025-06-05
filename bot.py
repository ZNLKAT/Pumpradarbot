bot.py
import requests
import time
from telegram import Bot

BOT_TOKEN = '7988462821:AAHoXUV1fhfu-gIcQXO5lYgworyAvMzGvGE'
CHAT_ID = 1093230583
CHECK_INTERVAL = 60  # Sekunden

bot = Bot(token=BOT_TOKEN)
last_data = {}

def get_tickers():
    url = "https://api.kucoin.com/api/v1/market/allTickers"
    response = requests.get(url)
    return response.json()["data"]["ticker"]

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
            price_change = ((price - old_price) / old_price) * 100 if old_price else 0
            vol_change = ((vol - old_vol) / old_vol) * 100 if old_vol else 0

            if 0.5 <= price_change <= 1.5 and vol_change >= 40:
                message = f"⚠️ Frühwarnung: {symbol}\n📈 Preis: +{price_change:.2f}%\n📊 Volumen: +{vol_change:.2f}%\n💰 Preis: {price} USDT"
                bot.send_message(chat_id=CHAT_ID, text=message)

        last_data[symbol] = {'price': price, 'vol': vol}

bot.send_message(chat_id=CHAT_ID, text="✅ PumpRadar Frühwarn-Bot ist aktiv.")

while True:
    try:
        tickers = get_tickers()
        scan_for_early_gainers(tickers)
        time.sleep(CHECK_INTERVAL)
    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f"Fehler: {e}")
        time.sleep(60)
