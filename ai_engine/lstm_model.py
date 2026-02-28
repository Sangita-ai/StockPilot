import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler

model = None

def predict_lstm(df):
    global model

    try:
        from tensorflow.keras.models import load_model
    except:
        return None

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "lstm_model.h5")

    if not os.path.exists(MODEL_PATH):
        print("LSTM model file not found")
        return None

   
    if model is None:
        try:
            model = load_model(MODEL_PATH)
            print("LSTM model loaded successfully")
        except Exception as e:
            print("Error loading LSTM:", e)
            return None

    try:
        data = df["Close"].values.reshape(-1, 1)
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(data)

        seq_len = 60
        if len(scaled) < seq_len:
            return None

        last_seq = scaled[-seq_len:]
        last_seq = last_seq.reshape(1, seq_len, 1)

        pred = model.predict(last_seq, verbose=0)
        pred_price = scaler.inverse_transform(pred)

        return float(pred_price[0][0])
    except Exception as e:
        print("Prediction error:", e)
        return None

    