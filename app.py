from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

print("Ladowanie modelu i wektoryzatora...")
try:
    model = joblib.load('sqli_rf_model.joblib')
    vectorizer = joblib.load('tfidf_vectorizer.joblib')
    print("Pomyslnie zaladowano model i wektoryzator.")
except Exception as e:
    print(f"Blad podczas ladowania modelu lub wektoryzatora: {e}")
    model = None
    vectorizer = None

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Backend dziala. Uzyj /api/login do uwierzytelniania."}), 200

@app.route('/api/login', methods=['POST'])
def login():
    if not model or not vectorizer:
        return jsonify({"message": "Blad serwera: Model ML nie zostal zaladowany."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"message": "Nieprawidlowe zadanie."}), 400

    login_val = data.get('login', '')
    password_val = data.get('password', '')

    # Wektoryzacja pol wejsciowych
    try:
        login_vec = vectorizer.transform([login_val])
        password_vec = vectorizer.transform([password_val])
        
        # Predykcja
        # prediction == 1 oznacza wykrycie ataku SQLi
        login_pred = model.predict(login_vec)[0]
        password_pred = model.predict(password_vec)[0]
    except Exception as e:
        print(f"Blad podczas predykcji: {e}")
        return jsonify({"message": "Blad serwera podczas analizy."}), 500

    if login_pred == 1 or password_pred == 1:
        print("Wykryto i zablokowano atak SQL Injection!")
        return jsonify({"message": "System zablokowal zadanie. Wykryto atak SQL Injection!"}), 403

    # Symulacja logiki logowania dla "czystych" danych
    if login_val == 'admin' and password_val == 'admin':
        return jsonify({"message": "Zalogowano pomyslnie!"}), 200
    else:
        return jsonify({"message": "Bledne dane logowania."}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
