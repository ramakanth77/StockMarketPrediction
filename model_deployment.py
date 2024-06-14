import pandas as pd
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import joblib

app = Flask(__name__)

def load_data(filename):
    try:
        data = pd.read_csv(filename, index_col='Date', parse_dates=True)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def create_sequences(data, seq_length):
    try:
        xs = []
        for i in range(len(data) - seq_length):
            x = data.iloc[i:(i + seq_length)].values
            xs.append(x)
        return np.array(xs)
    except Exception as e:
        print(f"Error creating sequences: {e}")
        return None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json()
        ticker = json_data['ticker']
        days = json_data['days']

        filename = f'{ticker}_stock_data_processed.csv'
        data = load_data(filename)
        if data is None:
            return jsonify({'error': 'Error loading data.'}), 400

        model = load_model(f'{ticker}_lstm_model.h5')
        scaler = joblib.load(f'{ticker}_scaler.gz')

        seq_length = 50
        X = create_sequences(data[['Close']], seq_length)
        if X is None:
            return jsonify({'error': 'Error creating sequences.'}), 400

        predictions = model.predict(X[-days:])
        predictions = scaler.inverse_transform(predictions)

        return jsonify({'predictions': predictions.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
