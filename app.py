from flask import Flask, request
from telegram import Bot
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

# Webhook endpoint (ham veri ile, debug ile)
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.data.decode('utf-8')  # Ham veriyi string olarak al
    message = data  # TradingView'den gelen ham mesajı kullan
    print(f"Received message: {message}")  # Debug mesajı

    # Mesajda hangi konuya ait olduğunu kontrol et
    topic_id = None
    for topic_name, tid in TOPIC_IDS.items():
        if topic_name.lower() in message.lower():
            topic_id = tid
            break

    # Mesajı ilgili konuya gönder
    if topic_id:
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            message_thread_id=topic_id
        )
        print(f"Sent to topic_id: {topic_id}")  # Debug mesajı
    else:
        bot.send_message(
            chat_id=CHAT_ID,
            text=f"Bilinmeyen konu: {message}"
        )
        print("Sent to default topic")  # Debug mesajı

    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
