from flask import Flask, request, jsonify
import requests
import os
import threading
import time
import json

app = Flask(__name__)

# Bot ve grup bilgileri
TELEGRAM_TOKEN = "7338866674:AAFF98ZTBvVtD1826gVGvdcx5usPouco4C0"
CHAT_ID = "-1002781192694"
TOPICS = {
    "2": "SMC",
    "4": "Out Side Bar",
    "6": "Asistant",
    "8": "Long Short",
    "10": "Duble Rsi"
}
PING_URL = "https://tradingview-bot-b8jr.onrender.com/webhook"  # Render URL'si

# Botu uyandırmak için ping mekanizması
def keep_alive():
    while True:
        time.sleep(14 * 60)  # 14 dakika bekle (15 dakikalık uyku sınırından az)
        try:
            requests.get(PING_URL)
            print("Ping sent to keep alive")
        except Exception as e:
            print(f"Ping failed: {e}")

# Sağlık kontrolü endpoint'i
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Webhook endpoint'i
@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook received:", request.get_data())  # Loglama
    data = request.get_json(force=True)  # JSON parse hatasını önler
    if data:
        raw_message = str(data)  # Ham veriyi string'e çevir
        print(f"Sending raw message: {raw_message}")
        send_telegram_message(CHAT_ID, "0", raw_message)  # Tüm gruba ham veri
        try:
            json_message = json.dumps(data, ensure_ascii=False)  # JSON formatına çevir
            print(f"Sending JSON message: {json_message}")
            for thread_id, topic in TOPICS.items():
                if topic.lower() in raw_message.lower() or f"#{topic.lower()}" in raw_message.lower():
                    send_telegram_message(CHAT_ID, thread_id, json_message)  # Konuya göre JSON
        except Exception as e:
            print(f"JSON error: {e}")
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "No data"}), 400

# Telegram'a mesaj gönderme fonksiyonu
def send_telegram_message(chat_id, thread_id, text):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "message_thread_id": thread_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(telegram_url, json=payload)
    print(f"Telegram response: {response.status_code} - {response.text}")  # Telegram yanıtı logla
    return response

if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))  # Render portu 10000
    app.run(host='0.0.0.0', port=port)
