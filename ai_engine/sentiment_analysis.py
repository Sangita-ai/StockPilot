from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob


NEWS_API_KEY = "dccc3cec502a4c62b8e5573f656fc7e8"

newsapi = NewsApiClient(api_key="dccc3cec502a4c62b8e5573f656fc7e8")
analyzer = SentimentIntensityAnalyzer()


def get_news_sentiment(ticker: str):
    articles = newsapi.get_everything(q=ticker, language='en', page_size=10)

    sentiments = []

    for article in articles["articles"]:
        text = article["title"] + " " + (article["description"] or "")
        score = analyzer.polarity_scores(text)
        sentiments.append(score["compound"])

    if not sentiments:
        return {"score": 0, "label": "Neutral"}

    avg_score = sum(sentiments) / len(sentiments)

    if avg_score > 0.2:
        label = "Bullish"
    elif avg_score < -0.2:
        label = "Bearish"
    else:
        label = "Neutral"

    return {
        "score": round(avg_score, 3),
        "label": label
    }




api = NewsApiClient(api_key="dccc3cec502a4c62b8e5573f656fc7e8")

def get_news_sentiment(ticker):
    articles = api.get_everything(q=ticker, language="en")
    score = 0
    count = 0

    for a in articles["articles"]:
        if a["description"]:
            blob = TextBlob(a["description"])
            score += blob.sentiment.polarity
            count += 1

    avg = score / count if count else 0
    label = "Bullish" if avg > 0 else "Bearish" if avg < 0 else "Neutral"

    return {"label": label, "score": avg}