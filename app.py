from flask import Flask, request
from telegram import Bot
import os

app = Flask(__name__)

# Bot ve grup bilgileri
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = Bot(token=TELEGRAM_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.data.decode('utf-8')
    print(f"Received data: {data}")  # Ham veriyi logla
    bot.send_message(chat_id=CHAT_ID, text=data)  # Doğrudan mesaj gönder
    print("Message sent to chat")  # Gönderim logu
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
