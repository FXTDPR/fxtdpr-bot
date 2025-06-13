from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import logging

# Logging ayarı
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask ve bot tanımlamaları
app = Flask(__name__)

# Token ve grup ID’si sabit tanımlı (test için)
TELEGRAM_TOKEN = "7338866674:AAFF98ZTBvVtD1826gVGvdcx5usPouco4C0"  # Bot token’ı
CHAT_ID = "-1002781192694"  # Grup ID’si

# Bot ve Application tanımla
bot = Bot(token=TELEGRAM_TOKEN)
application = Application.builder().token(TELEGRAM_TOKEN).build()

# /start komutunu işleyen fonksiyon
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Merhaba! Ben FXTDPR Trading Botuyum.')
    logger.info("Start command received from %s", update.effective_user.id)

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    application.process_update(update)
    return {"status": "ok"}, 200

# Komut handler’ını ekle
application.add_handler(CommandHandler("start", start))

# Webhook URL’sini ayarla
def set_webhook():
    url = f"https://fxtdpr-bot.onrender.com/webhook"
    bot.set_webhook(url=url)
    logger.info("Webhook set to %s", url)

if __name__ == "__main__":
    set_webhook()  # Webhook’u ayarla
    app.run(host="0.0.0.0", port=5000)
