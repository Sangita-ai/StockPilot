import numpy as np

def calculate_risk(df):

    try:
        df = df.copy()
        df.loc[:, "returns"] = df["Close"].pct_change()

        df = df.dropna()

        if len(df) == 0:
            return {}

        volatility = df["returns"].std() * (252 ** 0.5)

        cumulative = (1 + df["returns"]).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        max_drawdown = drawdown.min()

        if volatility is None or np.isnan(volatility):
            volatility = 0

        if volatility < 0.15:
            risk_level = "Low"
        elif volatility < 0.30:
            risk_level = "Medium"
        else:
            risk_level = "High"

        return {
            "volatility": float(volatility),
            "risk_level": risk_level,
            "max_drawdown": float(max_drawdown) if not np.isnan(max_drawdown) else 0,
            "risk_score": float(volatility * 100)
        }

    except:
        return {}
