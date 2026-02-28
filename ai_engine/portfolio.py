import json
from data_pipeline.stock_fetcher import get_stock_data

DB_PATH = "database/portfolio.json"


def load_portfolio():
    with open(DB_PATH, "r") as f:
        return json.load(f)


def save_portfolio(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)


def add_stock(ticker, quantity, buy_price):
    portfolio = load_portfolio()

    portfolio.append({
        "ticker": ticker,
        "quantity": quantity,
        "buy_price": buy_price
    })

    save_portfolio(portfolio)


def get_portfolio_summary():
    portfolio = load_portfolio()
    summary = []

    total_value = 0
    total_invested = 0

    for stock in portfolio:
        ticker = stock["ticker"]
        qty = stock["quantity"]
        buy_price = stock["buy_price"]

        df = get_stock_data(ticker)

        if df is None:
            continue

        current_price = df["Close"].iloc[-1]

        invested = qty * buy_price
        value = qty * current_price
        pnl = value - invested

        total_value += value
        total_invested += invested

        summary.append({
            "ticker": ticker,
            "quantity": qty,
            "buy_price": buy_price,
            "current_price": round(current_price, 2),
            "pnl": round(pnl, 2)
        })

    total_pnl = total_value - total_invested

    return {
        "stocks": summary,
        "total_invested": round(total_invested, 2),
        "total_value": round(total_value, 2),
        "total_pnl": round(total_pnl, 2)
    }
