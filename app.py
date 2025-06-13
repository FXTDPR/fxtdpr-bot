from flask import Flask, request
from telegram import Bot
import os

app = Flask(__name__)
app.debug = True  # Debug modunu aç

# Bot ve grup bilgileri (ortam değişkenlerinden alınacak)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = Bot(token=TELEGRAM_TOKEN)

# Webhook endpoint (senkron, hata yakalamalı)
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.data.decode('utf-8')  # Ham veriyi string olarak al
    print(f"Received data: {data}")  # Debug mesajı

    try:
        bot.send_message(chat_id=CHAT_ID, text=data)  # Senkron olarak gönder
        print("Message sent to chat")  # Gönderim logu
    except Exception as e:
        print(f"Error sending message: {e}")  # Hata logu

    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
