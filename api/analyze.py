from fastapi import FastAPI
from data_pipeline.stock_fetcher import get_stock_data
from ai_engine.technical_analysis import add_indicators, generate_signal

app = FastAPI()

@app.get("/api/analyze/{ticker}")
def analyze_stock(ticker: str):

    df = get_stock_data(ticker)

    if df is None:
        return {"error": "Invalid ticker"}

    df = add_indicators(df)

    signal = generate_signal(df)

    price = df["Close"].iloc[-1]

    return {
        "ticker": ticker,
        "price": float(price),
        "signal": signal
    }