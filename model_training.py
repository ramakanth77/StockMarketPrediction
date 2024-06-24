import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


def train_model(sequences, seq_length):
    X = sequences[:, :-1, :]
    y = sequences[:, -1, 3]  # Predicting the closing price

    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(seq_length - 1, X.shape[2])),
        LSTM(64),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)
    return model
