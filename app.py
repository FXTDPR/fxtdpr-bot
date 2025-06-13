from flask import Flask, request
from telegram import Bot
import asyncio
import os

app = Flask(__name__)

# Bot ve grup bilgileri (ortam değişkenlerinden alınacak)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
TOPIC_IDS = {
    "Duble Rsi": 10,
    "Long Short Pro Fast": 8,
    "My Asistant": 6,
    "Out Side Bar": 4,
    "SMC PRO": 2
}

bot = Bot(token=TELEGRAM_TOKEN)

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
async def webhook():
    data = request.json
    message = data.get('message', '')

    # Mesajda hangi konuya ait olduğunu kontrol et
    topic_id = None
    for topic_name, tid in TOPIC_IDS.items():
        if topic_name.lower() in message.lower():  # Büyük/küçük harfe duyarsız kontrol
            topic_id = tid
            break

    # Mesajı ilgili konuya gönder
    if topic_id:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            message_thread_id=topic_id
        )
    else:
        # Bilinmeyen konu için genel mesaj
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"Bilinmeyen konu: {message}"
        )

    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
