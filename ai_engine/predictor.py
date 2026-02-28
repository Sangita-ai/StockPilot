from sklearn.linear_model import LinearRegression
import numpy as np

def predict_next_price(df):

    try:
        df = df.copy()
        df = df.dropna()

        
        if len(df) < 20:
            return None

        df["day"] = np.arange(len(df))

        X = df[["day"]]
        y = df["Close"]

        if len(X) == 0 or len(y) == 0:
            return None

        model = LinearRegression()
        model.fit(X, y)

        next_day = np.array([[len(df)]])
        pred = model.predict(next_day)

        return float(pred[0])

    except Exception as e:
        print("Prediction error:", e)
        return None
