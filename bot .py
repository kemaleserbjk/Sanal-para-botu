import ccxt
import pandas as pd
import ta
import telegram
import time
import os

# Telegram ayarları
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=TELEGRAM_TOKEN)
exchange = ccxt.binance()

# 150 coinlik liste
COINS = [
    "BTC/USDT","ETH/USDT","XRP/USDT","SOL/USDT","DOGE/USDT",
    "ADA/USDT","BNB/USDT","LTC/USDT","LINK/USDT","DOT/USDT",
    "UNI/USDT","MATIC/USDT","VET/USDT","ICP/USDT","FTM/USDT",
    "XLM/USDT","THETA/USDT","FIL/USDT","TRX/USDT","EOS/USDT",
    "AAVE/USDT","CAKE/USDT","CHZ/USDT","SUSHI/USDT","KSM/USDT",
    "MKR/USDT","COMP/USDT","ENJ/USDT","ZRX/USDT","BAT/USDT",
    "ALGO/USDT","NEO/USDT","QTUM/USDT","OMG/USDT","DASH/USDT",
    "YFI/USDT","1INCH/USDT","RUNE/USDT","GRT/USDT","ANKR/USDT",
    "BTS/USDT","DCR/USDT","ETC/USDT","FTT/USDT","HNT/USDT",
    "KAVA/USDT","KNC/USDT","LOOM/USDT","LRC/USDT","MANA/USDT",
    "OCEAN/USDT","REN/USDT","RVN/USDT","SAND/USDT","SNX/USDT",
    "STMX/USDT","STORJ/USDT","TOMO/USDT","WAVES/USDT","XMR/USDT",
    "XTZ/USDT","ZEC/USDT","ZIL/USDT","AR/USDT","BAND/USDT",
    "COTI/USDT","CREAM/USDT","FET/USDT","LEND/USDT","NKN/USDT",
    "POWR/USDT","REP/USDT","STRAX/USDT","UMA/USDT","WTC/USDT",
    "ZRX/USDT","BNT/USDT","CVC/USDT","GNO/USDT","ICX/USDT",
    "MITH/USDT","NPXS/USDT","QTUM/USDT","SC/USDT","STORJ/USDT",
    "STRAT/USDT","TROY/USDT","UTK/USDT","WRX/USDT","ELF/USDT",
    "FIO/USDT","ICX/USDT","LRC/USDT","MITH/USDT","NPXS/USDT",
    "POWR/USDT","QTUM/USDT","REP/USDT","SC/USDT","STRAT/USDT",
    "STORJ/USDT","THETA/USDT","TOMO/USDT","WAN/USDT","WAVES/USDT",
    "XEM/USDT","XLM/USDT","XMR/USDT","XRP/USDT","XTZ/USDT",
    "ZEC/USDT","ZIL/USDT","SOL/USDT","ADA/USDT","BNB/USDT",
    "DOGE/USDT","LTC/USDT","LINK/USDT","DOT/USDT","UNI/USDT",
    "MATIC/USDT","VET/USDT","ICP/USDT","FTM/USDT","AAVE/USDT",
    "CAKE/USDT","CHZ/USDT","SUSHI/USDT","MKR/USDT","COMP/USDT",
    "ENJ/USDT","BAT/USDT","1INCH/USDT","RUNE/USDT","GRT/USDT",
    "ANKR/USDT","ALGO/USDT","NEO/USDT","QTUM/USDT","OMG/USDT",
    "DASH/USDT","YFI/USDT","RVN/USDT"
]

def check_macd(symbol):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe="3d", limit=100)
        df = pd.DataFrame(ohlcv, columns=['time','open','high','low','close','volume'])

        macd = ta.trend.MACD(df['close'])
        df['macd'] = macd.macd()
        df['signal'] = macd.macd_signal()

        last_macd = df['macd'].iloc[-1]
        last_signal = df['signal'].iloc[-1]

        return last_macd > last_signal
    except Exception as e:
        print(f"Hata {symbol}: {e}")
        return False

while True:
    for coin in COINS:
        if check_macd(coin):
            bot.send_message(chat_id=CHAT_ID, text=f"✅ {coin} 3D MACD YEŞİL YAKTI!")
            print(f"{coin} yeşil yaktı!")
        else:
            print(f"{coin} sinyal yok.")
    time.sleep(3600)  # 1 saatte bir kontrol
