from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup (SQLite)
DATABASE = 'transactions.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (amount REAL, network_status TEXT, time TEXT, prediction TEXT, alert TEXT)''')
    conn.commit()
    conn.close()

# Endpoint to process transaction prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get form data from frontend
    data = request.get_json()
    amount = data.get('amount')
    network_status = data.get('network_status')
    time = data.get('time')

    # Call the Java prediction logic
    result = predict_transaction(amount, network_status)

    # Store transaction details in the database
    store_transaction(amount, network_status, time, result['prediction'], result['alert'])

    # Return prediction result and alert to the frontend
    return jsonify(result)

# Function to call Java code for prediction
def predict_transaction(amount, network_status):
    # Assuming the Java logic file 'PredictTransaction.java' is compiled and ready to use
    prediction_logic = f'java PredictTransaction {amount} {network_status}'
    prediction_output = subprocess.check_output(prediction_logic, shell=True).decode()

    # Parse the output
    prediction, alert = parse_prediction_output(prediction_output)

    return {
        'prediction': prediction,
        'alert': alert
    }

# Function to parse the plain text output from the Java program
def parse_prediction_output(output):
    # Assuming output format is:
    # PREDICTION: <prediction message>
    # ALERT: <alert message>
    lines = output.split('\n')
    prediction = ""
    alert = ""

    for line in lines:
        if line.startswith("PREDICTION:"):
            prediction = line.replace("PREDICTION:", "").strip()
        elif line.startswith("ALERT:"):
            alert = line.replace("ALERT:", "").strip()

    return prediction, alert

# Store transaction in the database
def store_transaction(amount, network_status, time, prediction, alert):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO transactions (amount, network_status, time, prediction, alert) VALUES (?, ?, ?, ?, ?)',
              (amount, network_status, time, prediction, alert))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
