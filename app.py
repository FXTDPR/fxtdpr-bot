from flask import Flask, request, jsonify
import requests
import os
import threading
import time
import json
import re

app = Flask(__name__)

TELEGRAM_TOKEN = "7338866674:AAFF98ZTBvVtD1826gVGvdcx5usPouco4C0"
CHAT_ID = "-1002781192694"
TOPICS = {
    "2": "SMC",
    "4": "Out Side Bar",
    "6": "Asistant",
    "8": "Long Short",
    "10": "Duble Rsi"
}
PING_URL = "https://tradingview-bot-b8jr.onrender.com/webhook"

def keep_alive():
    while True:
        time.sleep(14 * 60)
        try:
            requests.get(PING_URL)
            print("Ping sent to keep alive")
        except Exception as e:
            print(f"Ping failed: {e}")

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook received - Headers:", dict(request.headers))
    print("Webhook received - Raw data:", request.get_data().decode('utf-8'))
    try:
        data = request.get_json(force=True, silent=True)
        print("Parsed JSON data:", data)
        raw_data = request.get_data().decode('utf-8')
        if data or raw_data:
            if raw_data:
                # Yeni format için regex
                match = re.match(r"#(.+?)\s*:\s*(\d+)\nAlarm Türü: (.+?)\nKapanış Fiyatı: (\d+\.\d+)(?:\n(.+))?", raw_data, re.DOTALL)
                if match:
                    ticker, interval, detail, price, extra = match.groups() if match.groups()[-1] else (match.groups()[:-1] + ('',))
                    formatted_message = f"*{ticker} {interval} Sinyali*\n" \
                                      f"Fiyat: {price}\n" \
                                      f"Detay: {detail}\n" \
                                      f"Ekstra: {extra.strip() if extra else 'Yok'}"
                else:
                    formatted_message = raw_data  # Parse edilemezse ham hali
            elif data:
                formatted_message = f"*{data.get('ticker', 'Unknown')} {data.get('interval', 'Unknown')} Sinyali*\n" \
                                  f"Fiyat: {data.get('price', 'Unknown')}\n" \
                                  f"Detay: {data.get('detail', 'Unknown')}"
            print(f"Sending formatted message: {formatted_message}")
            topic_match = False
            try:
                for thread_id, topic_name in TOPICS.items():
                    if topic_name.lower() in raw_data.lower() or (match and ticker.lower() == topic_name.lower()):
                        topic_match = True
                        send_telegram_message(CHAT_ID, thread_id, formatted_message)
                if not topic_match and ('#outside' in raw_data.lower() or data and data.get('#outside')):
                    send_telegram_message(CHAT_ID, "4", formatted_message)
            except Exception as e:
                print(f"JSON error: {e}")
            return jsonify({"status": "success"}), 200
        else:
            print("No valid data")
            return jsonify({"status": "error", "message": "No data"}), 400
    except Exception as e:
        print(f"Parse error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

def send_telegram_message(chat_id, thread_id, text):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "message_thread_id": thread_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(telegram_url, json=payload)
    print(f"Telegram response: {response.status_code} - {response.text}")
    return response

if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
