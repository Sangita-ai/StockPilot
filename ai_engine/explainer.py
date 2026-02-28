def generate_explanation(signal, sentiment, df):
    details = []

    try:
        if signal == "Bullish":
            details.append("Moving averages indicate upward trend.")
        elif signal == "Bearish":
            details.append("Moving averages indicate downward trend.")
        else:
            details.append("Trend is neutral.")

        if sentiment["label"] == "Bullish":
            details.append("News sentiment is positive.")
        elif sentiment["label"] == "Bearish":
            details.append("News sentiment is negative.")

        summary = f"Overall signal is {signal}."

        return {
            "details": details,
            "summary": summary
        }

    except:
        return {
            "details": ["AI explanation unavailable"],
            "summary": "Could not generate explanation"
        }
