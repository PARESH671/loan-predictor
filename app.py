from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

model = joblib.load('loan_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = [[
            float(data.get('income', 0)),
            int(data.get('age', 0)),
            int(data.get('credit_score', 0)),
            float(data.get('loan_amount', 0))
        ]]
        
        prediction = model.predict(features)
        status = "Eligible ✅" if prediction[0] == 1 else "Not Eligible ❌"
        return jsonify({"status": status})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)