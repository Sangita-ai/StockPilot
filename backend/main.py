from fastapi import FastAPI
import math

from data_pipeline.stock_fetcher import get_stock_data, get_basic_info
from ai_engine.technical_analysis import add_indicators, generate_signal
from ai_engine.predictor import predict_next_price
from ai_engine.sentiment_analysis import get_news_sentiment
from ai_engine.explainer import generate_explanation
from ai_engine.portfolio import add_stock, get_portfolio_summary
from ai_engine.risk_engine import calculate_risk
from ai_engine.lstm_model import predict_lstm
from ai_engine.backtester import run_backtest
from ai_engine.alerts import add_alert, check_alerts


app = FastAPI(title="StockPilot")



def safe(v):
    """Convert NaN/inf to None so JSON won't crash"""
    try:
        if v is None:
            return None
        if isinstance(v, float):
            if math.isnan(v) or math.isinf(v):
                return None
        return float(v) if isinstance(v, (int, float)) else v
    except:
        return None



@app.get("/")
def home():
    return {"message": "StockPilot AI backend running"}



@app.get("/analyze/{ticker}")
def analyze_stock(ticker: str):

    try:
        df = get_stock_data(ticker)

        if df is None or df.empty:
            return {"error": "Invalid ticker"}

       
        try:
            df = add_indicators(df)
        except:
            pass

        
        try:
            signal = generate_signal(df)
        except:
            signal = "Neutral"

        
        try:
            prediction = predict_next_price(df)
        except:
            prediction = None

        
        try:
            lstm_prediction = predict_lstm(df)
        except:
            lstm_prediction = None

       
        try:
            sentiment = get_news_sentiment(ticker)
        except:
            sentiment = {"label": "Neutral", "score": 0}

       
        try:
            risk = calculate_risk(df)
        except:
            risk = {}

        
        try:
            backtest = run_backtest(df)
        except:
            backtest = {}

        
        try:
            explanation = generate_explanation(signal, sentiment, df)
        except:
            explanation = {"details": [], "summary": ""}

       
        try:
            info = get_basic_info(ticker)
        except:
            info = {}

        
        return {
            "ticker": ticker,
            "signal": signal,
            "predicted_price": safe(prediction),
            "lstm_prediction": safe(lstm_prediction),
            "info": info,
            "sentiment": sentiment,
            "explanation": explanation,
            "risk": {
                "volatility": safe(risk.get("volatility")) if risk else None,
                "risk_level": risk.get("risk_level") if risk else None,
                "max_drawdown": safe(risk.get("max_drawdown")) if risk else None,
                "risk_score": safe(risk.get("risk_score")) if risk else None,
            } if risk else {},
            "backtest": {
                "final_value": safe(backtest.get("final_value")) if backtest else None,
                "profit": safe(backtest.get("profit")) if backtest else None,
            } if backtest else {}
        }

    except Exception as e:
        print("SERVER ERROR:", e)
        return {"error": str(e)}



@app.post("/portfolio/add")
def add_to_portfolio(ticker: str, quantity: int, buy_price: float):
    add_stock(ticker, quantity, buy_price)
    return {"message": "Stock added"}


@app.get("/portfolio")
def portfolio():
    return get_portfolio_summary()



@app.post("/alert/add")
def add_price_alert(ticker: str, target: float):
    add_alert(ticker, target)
    return {"message": "Alert added"}


@app.get("/alert/check")
def check_price_alerts():
    return check_alerts()

@app.post("/webhook/alert")
def webhook_alert(data: dict):
    ticker = data.get("ticker")
    target = float(data.get("target"))
    add_alert(ticker, target)
    return {"status": "Webhook alert added"}