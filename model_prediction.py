import numpy as np
import tensorflow as tf

def predict_next_sequence(model, last_sequence, scaler):
    last_sequence = np.expand_dims(last_sequence, axis=0)
    prediction = model.predict(last_sequence)
    prediction = np.concatenate((last_sequence[:, -1, :-1], prediction), axis=2)
    prediction = scaler.inverse_transform(prediction.reshape(-1, prediction.shape[2]))
    return prediction[0, -1]
