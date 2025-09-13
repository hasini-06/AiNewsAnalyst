import requests
from groq import Groq
import streamlit as st
import re
import html

def clean_text(raw):
    """Remove HTML tags and decode entities."""
    if not raw:
        return ""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", raw)
    # Decode HTML entities (like &amp;)
    text = html.unescape(text)
    return text.strip()

# Initialize Groq client
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

def fetch_news(query="technology"):
    """Fetch latest news articles from NewsAPI"""
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        articles = r.json().get("articles", [])
        return [
            {
                "title": a["title"],
                "url": a["url"],
                "content": a.get("description") or a.get("content") or a["title"]
            }
            for a in articles[:5]
        ]
    return []

def analyze_with_groq(text, task="summary"):
    """Summarization or analysis with Groq LLM"""
    prompt = f"Task: {task}\nInput: {text}\nReturn concise output only."
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def sentiment_analysis(text):
    """Simple sentiment classification"""
    prompt = f"""
Classify the sentiment of the following text as strictly one of:
Positive, Negative, or Neutral.

Text: {text}

Answer with only one word: Positive, Negative, or Neutral.
"""
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",  
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3
    )
    return response.choices[0].message.content.strip()
