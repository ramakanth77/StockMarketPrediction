import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

def load_data(filename):
    try:
        data = pd.read_csv(filename, index_col='Date', parse_dates=True)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def create_sequences(data, seq_length):
    try:
        xs, ys = [], []
        for i in range(len(data) - seq_length):
            x = data.iloc[i:(i + seq_length)].values
            y = data.iloc[i + seq_length].values
            xs.append(x)
            ys.append(y)
        return np.array(xs), np.array(ys)
    except Exception as e:
        print(f"Error creating sequences: {e}")
        return None, None

def build_lstm_model(input_shape):
    try:
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
    except Exception as e:
        print(f"Error building LSTM model: {e}")
        return None

def evaluate_model(model, X_test, y_test):
    try:
        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        print(f"Mean Absolute Error: {mae}")
        print(f"Root Mean Squared Error: {rmse}")
    except Exception as e:
        print(f"Error evaluating model: {e}")

if __name__ == "__main__":
    filename = 'AAPL_stock_data_processed.csv'
    seq_length = 50

    data = load_data(filename)
    if data is not None:
        X, y = create_sequences(data[['Close']], seq_length)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        model = build_lstm_model((X_train.shape[1], X_train.shape[2]))
        if model is not None:
            model.fit(X_train, y_train, epochs=10, batch_size=32)
            evaluate_model(model, X_test, y_test)
