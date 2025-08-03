import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

# טען משתני סביבה
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

# התחברות ל-Bybit
session = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)

# פונקציה לקבלת מחיר ביטקוין
def get_btc_price():
    try:
        ticker = session.get_ticker(symbol="BTCUSDT")
        return ticker['result'][0]['lastPrice']
    except Exception as e:
        return f"שגיאה: {e}"

# פקודת /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 הבוט פועל! אתה מחובר לאיתותים בזמן אמת")

# פקודת /price
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_btc_price()
    await update.message.reply_text(f"📊 המחיר הנוכחי של BTC: {price} USDT")

# פונקציית הרצה
async def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    await app.run_polling()

# התחלת הבוט
if __name__ == "__main__":
    asyncio.run(main())