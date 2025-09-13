import streamlit as st
from rag_utils import fetch_news, analyze_with_groq, sentiment_analysis
from audio_utils import text_to_speech

# Page config
st.set_page_config(
    page_title="AI News Analyst",
    layout="wide",
    page_icon="📰"
)

# Title section
st.markdown("<h1 style='text-align:center; color:white;'>🤖 AI-Powered News & Research Analyst</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Stay ahead with AI-curated news summaries, sentiment insights & audio briefings.</p>", unsafe_allow_html=True)


if st.button("▶️ Play Today's Briefing"):
    audio_data = text_to_speech("Hello, this is your AI-powered briefing for today.")
    st.audio(audio_data, format="audio/wav")

st.markdown("---")

# News search section
st.subheader("📡 Search for Sector-Specific News")
query = st.text_input("Enter a sector/topic (e.g., AI, Finance, Healthcare)")

if st.button("🔍 Get News"):
    news = fetch_news(query=query)
    if news:
        st.session_state.news = news
    else:
        st.error("⚠️ No news found or API limit reached.")

# Display news articles
if "news" in st.session_state:
    st.subheader("📰 Latest News")
    for i, article in enumerate(st.session_state.news, start=1):
        with st.expander(f"{i}. {article['title']}"):
            st.write(article["content"])
            st.markdown(f"[🌐 Read full article]({article['url']})")

            summary = analyze_with_groq(article["content"], task="summary")
            st.markdown(f"**📌 Summary:** {summary}")

            sentiment = sentiment_analysis(article["content"])
            st.markdown(f"**💬 Sentiment:** {sentiment}")

            if st.button(f"🔊 Listen to Summary {i}"):
                audio_data = text_to_speech(summary)
                st.audio(audio_data, format="audio/wav")
                st.success("✅ Audio summary generated!")
