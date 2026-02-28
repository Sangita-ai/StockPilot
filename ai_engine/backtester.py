def run_backtest(df):

    try:
        df = df.copy()
        df = df.dropna().reset_index(drop=True)

        if len(df) < 30:  
            return {
                "final_value": 10000,
                "profit": 0
            }

        initial_balance = 10000
        balance = initial_balance
        shares = 0

        for i in range(1, len(df)):

            ma20 = df.loc[i, "MA20"]
            ma50 = df.loc[i, "MA50"]
            price = df.loc[i, "Close"]

            if ma20 > ma50 and shares == 0:
                shares = balance / price
                balance = 0

            elif ma20 < ma50 and shares > 0:
                balance = shares * price
                shares = 0

        final_value = balance if shares == 0 else shares * df.iloc[-1]["Close"]
        profit = final_value - initial_balance

        return {
            "final_value": round(final_value, 2),
            "profit": round(profit, 2)
        }

    except Exception as e:
        return {
            "final_value": 10000,
            "profit": 0
        }