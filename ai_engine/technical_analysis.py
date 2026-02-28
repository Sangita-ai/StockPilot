import pandas as pd

def add_indicators(df: pd.DataFrame):
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()

    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df


def generate_signal(df):

    if df is None or df.empty:
        return "Neutral"

    last = df.iloc[-1]

    if last["MA20"] > last["MA50"] and last["RSI"] > 55:
        return "Bullish"

    elif last["MA20"] < last["MA50"] and last["RSI"] < 45:
        return "Bearish"

    else:
        return "Neutral"
