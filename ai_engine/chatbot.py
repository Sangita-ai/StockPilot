from transformers import pipeline


generator = pipeline("text-generation", model="distilgpt2")

def generate_ai_response(data):
    prompt = f"""
    You are a stock market AI assistant.

    Signal: {data['signal']}
    Sentiment: {data['sentiment']['label']}
    Risk Level: {data['risk']['risk_level']}
    Predicted Price: {data['predicted_price']}

    Give a short recommendation for investor.
    """

    result = generator(prompt, max_length=120, num_return_sequences=1)

    return result[0]["generated_text"]