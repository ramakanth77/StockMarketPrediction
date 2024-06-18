import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def load_data(filename):
    try:
        data = pd.read_csv(filename, index_col='Date', parse_dates=True)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def handle_missing_values(data):
    try:
        data.fillna(method='ffill', inplace=True)
        data.fillna(method='bfill', inplace=True)
        return data
    except Exception as e:
        print(f"Error handling missing values: {e}")
        return None

def feature_engineering(data):
    try:
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['SMA_200'] = data['Close'].rolling(window=200).mean()
        data['Volatility'] = data['Close'].rolling(window=50).std()
        data['Momentum'] = data['Close'].diff(5)
        return data
    except Exception as e:
        print(f"Error in feature engineering: {e}")
        return None

def normalize_data(data):
    try:
        scaler = MinMaxScaler()
        data_scaled = pd.DataFrame(scaler.fit_transform(data), columns=data.columns, index=data.index)
        return data_scaled, scaler
    except Exception as e:
        print(f"Error in data normalization: {e}")
        return None, None

if __name__ == "__main__":
    filename = 'AAPL_stock_data.csv'
    processed_filename = 'AAPL_stock_data_processed.csv'

    data = load_data(filename)
    if data is not None:a)
        data = feature_engineering(data)
        data = handle_missing_values(dat
        data_scaled, scaler = normalize_data(data)
        if data_scaled is not None:
            data_scaled.to_csv(processed_filename)
            print(f"Processed data saved to {processed_filename}")
