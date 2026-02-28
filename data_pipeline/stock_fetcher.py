import yfinance as yf
import pandas as pd
from functools import lru_cache


@lru_cache(maxsize=50)
def get_stock_data(ticker: str):
    try:
        df = yf.download(
            ticker,
            period="6mo",
            interval="1d",
            auto_adjust=False,
            progress=False
        )

        if df is None or df.empty:
            return None

        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]

        df = df.reset_index()

        
        rename_map = {}
        for c in df.columns:
            if c.lower() == "open": rename_map[c] = "Open"
            if c.lower() == "high": rename_map[c] = "High"
            if c.lower() == "low": rename_map[c] = "Low"
            if c.lower() == "close": rename_map[c] = "Close"
            if c.lower() == "date": rename_map[c] = "Date"

        df.rename(columns=rename_map, inplace=True)

       
        required = ["Date", "Open", "High", "Low", "Close"]
        if not all(col in df.columns for col in required):
            print("Missing OHLC columns:", df.columns)
            return None

        return df

    except Exception as e:
        print("FETCH ERROR:", e)
        return None


def get_basic_info(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1d")

        price = None
        if not hist.empty:
            price = float(hist["Close"].iloc[-1])

        return {
            "name": info.get("longName", ticker),
            "sector": info.get("sector"),
            "marketCap": info.get("marketCap"),
            "currentPrice": info.get("currentPrice") or price,
            "peRatio": info.get("trailingPE")
        }
    except:
        return {}