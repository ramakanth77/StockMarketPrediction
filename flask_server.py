
from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from data_collection import fetch_stock_data
from data_preprocessing import preprocess_data, create_sequences
from model_training import train_model
from model_prediction import predict_next_sequence


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes




@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    try:
        data = request.get_json()
        ticker = data['ticker']
        period = data.get('period', '1d')  # Default to '1d' if not provided
        interval = data.get('interval', '1h')  # Default to '1h' if not provided

        stock_data = yf.download(ticker, period=period, interval=interval)

        if stock_data.empty:
            return jsonify({'error': 'No data found for the given ticker'}), 404

        stock_data.reset_index(inplace=True)
        stock_data.rename(columns={'Datetime': 'Date'}, inplace=True)
        stock_data = stock_data.to_dict(orient='records')
        return jsonify(stock_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict', methods=['POST'])
def predict():
    try:
        content = request.json
        ticker = content['ticker']

        # Fetch historical data
        stock_data = fetch_stock_data(ticker, period='max', interval='1d')

        # Preprocess the data
        scaled_data, scaler = preprocess_data(stock_data)

        # Create sequences
        seq_length = 50  # Example sequence length
        sequences = create_sequences(scaled_data, seq_length)

        # Train the model
        model = train_model(sequences, seq_length)

        # Predict the next sequence
        last_sequence = sequences[-1, :-1, :]  # Adjusting shape for the last sequence
        last_sequence = np.expand_dims(last_sequence, axis=0)
        prediction = model.predict(last_sequence)

        # Inverse transform the prediction
        prediction_with_features = np.zeros((prediction.shape[0], scaled_data.shape[1]))
        prediction_with_features[:, -1] = prediction[:, 0]  # Fill the last column with predictions
        prediction = scaler.inverse_transform(prediction_with_features)[:, -1]  # Inverse transform and get last column

        rounded_prediction = round(prediction[0], 2)  # Round the prediction to 2 decimal places

        return jsonify({'prediction': rounded_prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)