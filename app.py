from telegram.ext import Application, CommandHandler, ContextTypes
import os
import logging

# Logging ayarı
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot ve token tanımlamaları
TELEGRAM_TOKEN = "7338866674:AAFF98ZTBvVtD1826gVGvdcx5usPouco4C0"  # Token sabit (test için)
CHAT_ID = "-1002781192694"  # Grup ID’si

# Application tanımla
application = Application.builder().token(TELEGRAM_TOKEN).build()

# /start komutunu işleyen fonksiyon
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Merhaba! Ben FXTDPR Trading Botuyum.')
    logger.info("Start command received from %s", update.effective_user.id)

# Botu başlat
def main():
    # Komut handler’ını ekle
    application.add_handler(CommandHandler("start", start))

    # Polling ile botu çalıştır
    application.run_polling()

if __name__ == "__main__":
    main()
