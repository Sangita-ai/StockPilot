# 🚀 StockPilot  
### A Smart & Simple AI-Based Stock Analysis Dashboard

StockPilot is a personal project I built to explore how AI can be applied to financial data in a practical and beginner-friendly way.

The idea was simple:  
Can we combine technical analysis, machine learning, deep learning, and real-time data into one clean dashboard that anyone can understand?

StockPilot is the result.

It is not meant to replace professional trading tools.  
It is built to demonstrate AI integration, system design, and full-stack development in a real-world scenario.

---

## 🌟 What StockPilot Can Do

- 📊 Show interactive candlestick charts  
- 📈 Analyze trends using moving averages (MA20 & MA50)  
- 🤖 Predict next-day price using a Machine Learning model  
- 🧠 Forecast trends using an LSTM deep learning model  
- 📉 Calculate risk and volatility  
- 📊 Run simple backtesting on historical data  
- 📰 Provide market sentiment insight  
- 📁 Track a basic stock portfolio  
- 🔔 Set price alerts  
- 🌍 Monitor major market indices  

Everything is combined into a clean Streamlit dashboard powered by a FastAPI backend.

---

## 🛠 Tech Used

- FastAPI – Backend API  
- Streamlit – Interactive dashboard  
- yFinance – Real-time market data  
- Scikit-learn – Machine Learning model  
- TensorFlow – LSTM Deep Learning  
- Plotly – Financial charts  
- Pandas & NumPy – Data processing  

---

# ▶ How To Run The Project

1️⃣ Clone or Download

git clone https://github.com/Sangita-ai/StockPilot.git

cd StockPilot

2️⃣ Install Requirements

Make sure Python is installed (3.9+ recommended).

Run: pip install -r requirements.txt

### 3️⃣ Start Backend Server

uvicorn backend.main:app --reload

you should see: Uvicorn running on http://127.0.0.1:8000

Keep this terminal open.

### 4️⃣ Open the Dashboard

Open a new terminal and run: python -m streamlit run frontend/app.py

Your browser will open automatically.

## 📌 Stocks You Can Try

Indian Stocks:

RELIANCE.NS
TCS.NS
SBIN.NS
INFY.NS

US Stocks:

AAPL
MSFT
TSLA
NVDA

---

## 🎯 Why I Built This

I wanted to build something that combines:

- AI models
- Financial data
- Backend API design
- Dashboard development
- Real-world use case

StockPilot is my attempt to bring all of that into one structured system.

This project reflects my interest in applying AI beyond theory — into practical systems.

---

👩‍💻 Built by Sangita Sharma 
