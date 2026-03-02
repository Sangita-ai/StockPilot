import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
import time
import datetime

from data_pipeline.stock_fetcher import get_stock_data
from ai_engine.technical_analysis import add_indicators

API_URL = "http://127.0.0.1:8000"


st.set_page_config(layout="wide", page_title="StockPilot")


st.markdown("""
<style>
.main {background-color: #0E1117;}
.title {font-size: 55px; font-weight: 800; color: #00FFB2;}
.subtitle {color: gray; font-size:18px;}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="title">StockPilot </div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Market Intelligence Terminal</div>', unsafe_allow_html=True)
st.divider()


@st.cache_data(ttl=30)
def fetch_data(symbol):
    try:
        r = requests.get(f"{API_URL}/analyze/{symbol}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if "error" not in data:
                return data
    except:
        pass
    return None



st.header("🌍 Market Overview")

indices = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "NASDAQ": "^IXIC",
    "S&P 500": "^GSPC"
}

cols = st.columns(4)

for i, (name, symbol) in enumerate(indices.items()):
    data = fetch_data(symbol)
    if data:
        price = data.get("info", {}).get("currentPrice")
        signal = data.get("signal")
        cols[i].metric(name, price, signal)
    else:
        cols[i].metric(name, "—", "—")

st.divider()


st.header("📊 Sector Watch")

sector_data = {
    "IT": ["TCS.NS", "INFY.NS"],
    "Banking": ["HDFCBANK.NS", "SBIN.NS"],
    "US Tech": ["AAPL", "MSFT"]
}

for sector, stocks in sector_data.items():
    st.subheader(sector)
    cols = st.columns(len(stocks))

    for i, s in enumerate(stocks):
        data = fetch_data(s)
        if data:
            price = data.get("info", {}).get("currentPrice")
            signal = data.get("signal")
            cols[i].metric(s, price, signal)
        else:
            cols[i].metric(s, "—", "—")

st.divider()


st.sidebar.header("⭐ Quick Select Stocks")

quick_stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "SBIN.NS",
    "AAPL", "TSLA", "MSFT"
]

for s in quick_stocks:
    if st.sidebar.button(s, key=f"quick_{s}"):
        st.session_state["selected_stock"] = s

st.sidebar.write("Last update:", datetime.datetime.now().strftime("%H:%M:%S"))


default_stock = st.session_state.get("selected_stock", "AAPL")
ticker = st.text_input("🔍 Search Stock", default_stock)

if ticker:

    result = fetch_data(ticker)

    if not result:
        st.error("Invalid ticker or backend issue.")
        st.stop()

    info = result.get("info", {})

    
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Price", info.get("currentPrice"))
    col2.metric("📈 Signal", result.get("signal"))
    col3.metric("⚠ Risk", result.get("risk", {}).get("risk_level"))
    col4.metric("📰 Sentiment", result.get("sentiment", {}).get("label"))

    st.divider()

    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Overview", "Chart", "AI Insights", "Portfolio", "Alerts"]
    )

    
    with tab1:
        st.subheader("Stock Information")
        st.write(info)

        st.subheader("Predicted Price")
        st.info(result.get("predicted_price"))

        st.subheader("LSTM Prediction")
        lstm = result.get("lstm_prediction")
        if lstm:
            st.success(round(lstm, 2))
        else:
            st.info("Model not available")

    
    with tab2:
        st.subheader("Candlestick Chart")

        df = get_stock_data(ticker)
        if df is not None and not df.empty:
            df = add_indicators(df)
            df = df.dropna()

            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=df["Date"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"]
            ))

            fig.update_layout(
                template="plotly_dark",
                height=600,
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(fig, use_container_width=True)

    
    with tab3:
        st.subheader("AI Explanation")
        explanation = result.get("explanation", {})
        for p in explanation.get("details", []):
            st.write("•", p)
        st.info(explanation.get("summary", ""))

        st.subheader("Risk Analysis")
        st.write(result.get("risk"))

        st.subheader("Backtest")
        st.write(result.get("backtest"))

    
    with tab4:
        st.subheader("Portfolio Manager")

        col1, col2, col3 = st.columns(3)

        p_ticker = col1.text_input("Ticker", key="portfolio_ticker")
        qty = col2.number_input("Qty", min_value=1, key="portfolio_qty")
        buy_price = col3.number_input("Buy Price", min_value=0.0, key="portfolio_price")

        if st.button("Add to Portfolio", key="add_portfolio"):
            requests.post(
                f"{API_URL}/portfolio/add",
                params={"ticker": p_ticker, "quantity": qty, "buy_price": buy_price}
            )
            st.success("Added")

        if st.button("Refresh Portfolio", key="refresh_portfolio"):
            data = requests.get(f"{API_URL}/portfolio").json()
            st.write("Total PnL:", data.get("total_pnl"))
            st.dataframe(data.get("stocks", []))

    
    with tab5:
        st.subheader("Price Alerts")

        a_ticker = st.text_input("Alert ticker", key="alert_ticker")
        target = st.number_input("Target price", key="alert_price")

        if st.button("Set Alert", key="set_alert"):
            requests.post(
                f"{API_URL}/alert/add",
                params={"ticker": a_ticker, "target": target}
            )
            st.success("Alert set")

        if st.button("Check Alerts", key="check_alerts"):
            alerts = requests.get(f"{API_URL}/alert/check").json()
            st.write(alerts)


st.subheader("📊 Candlestick Chart")

df = get_stock_data(ticker)

if df is None or df.empty:
    st.warning("No chart data available")
else:

    
    df = df.reset_index(drop=True)

    
    required_cols = ["Open", "High", "Low", "Close"]

    
    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        st.warning(f"Chart data missing columns: {missing}")
        st.stop()

    
    df = df.dropna(subset=required_cols)

    if len(df) < 5:
        st.warning("Not enough data for chart")
    else:
        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price"
        ))

        
        if "MA20" in df.columns:
            fig.add_trace(go.Scatter(
                x=df["Date"], y=df["MA20"],
                name="MA20", line=dict(color="cyan")
            ))

        if "MA50" in df.columns:
            fig.add_trace(go.Scatter(
                x=df["Date"], y=df["MA50"],
                name="MA50", line=dict(color="orange")
            ))

        fig.update_layout(
            template="plotly_dark",
            height=600,
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig, width="stretch")