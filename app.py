from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)

# --- 🔥 FIREBASE CONNECTION ---
# Tumhara Naya Database URL
DB_URL = "https://v1000-686c0-default-rtdb.firebaseio.com"

# --- 🔐 API 1: LOGIN CHECK (Via Firebase) ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user_key = data.get('key')

    if not user_key:
        return jsonify({"success": False, "message": "KEY MISSING"}), 400

    # Firebase se poocho: "Kya ye Key 'users' folder mein hai?"
    try:
        # Hum seedha us key ka status check karenge
        response = requests.get(f"{DB_URL}/users/{user_key}.json")
        status = response.json()  # Ye 'active' ya 'expired' return karega

        if status == "active":
            return jsonify({
                "success": True, 
                "message": "ACCESS GRANTED", 
                "plan": "VIP MEMBER"
            })
        elif status == "expired":
            return jsonify({"success": False, "message": "KEY EXPIRED"}), 403
        else:
            return jsonify({"success": False, "message": "INVALID KEY"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": "SERVER ERROR"}), 500


# --- 🔮 API 2: PREDICTION LOGIC (Wahi Secret Formula) ---
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        last_period = int(data.get('last_period'))
    except:
        return jsonify({"prediction": "ERROR", "confidence": 0})

    # --- SECRET LOGIC ---
    last_digit = int(str(last_period)[-1])
    
    # Logic: 60% Pattern, 40% Random
    chance = random.randint(1, 100)
    
    if chance > 40:
        if last_digit in [0, 2, 4, 6, 8]:
            prediction = "SMALL" # Red
        else:
            prediction = "BIG" # Green
    else:
        prediction = random.choice(["BIG", "SMALL"])

    return jsonify({
        "period": last_period + 1,
        "prediction": prediction,
        "confidence": random.randint(88, 99)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
