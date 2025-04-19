import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.generator import PostGenerator
from modules.analyzer import ContentAnalyzer
from modules.database import DBManager

def main():
    st.set_page_config(page_title="LinkedIn AI Content Creator", layout="wide")
    st.title("🚀 LinkedIn AI Content Creator")

    # Session state safety
    if "selected_post" not in st.session_state:
        st.session_state.selected_post = None

    pg = PostGenerator()
    analyzer = ContentAnalyzer()
    db = DBManager()

    with st.sidebar:
        st.header("Post Settings")
        topic = st.text_input("Enter post topic", value="AI in Tech")
        tone = st.selectbox("Select tone", ["Professional", "Casual", "Inspirational", "Technical"])
        cta = st.selectbox("Call-to-Action", ["Engage with comments", "Click link", "Share with network"])

    if st.button("✨ Generate Posts"):
        with st.spinner("Generating posts..."):
            posts = pg.generate_posts(topic, tone, cta)
            if not posts:
                st.warning("No posts generated. Try again later.")
                return

            for i, post in enumerate(posts):
                st.markdown(f"### Post {i+1}")
                st.write(post.get("content", ""))
                st.caption(f"Hashtags: {post.get('hashtags', '')}")
                if st.button(f"👍 Use Post {i+1}", key=f"use_{i}"):
                    db.log_feedback(i, True)
                    st.success("Feedback recorded! Post selected.")
                    st.session_state.selected_post = i

    st.sidebar.markdown("---")
    st.sidebar.header("📊 Trend Insights")
    top_topics = analyzer.get_top_topics(3)
    if top_topics:
        st.sidebar.subheader("Top Topics")
        for t in top_topics:
            st.sidebar.code(t)
    else:
        st.sidebar.write("No data for topics yet.")

    optimal_times = analyzer.get_optimal_times()
    if not optimal_times.empty:
        st.sidebar.subheader("Best Posting Times")
        st.sidebar.dataframe(optimal_times[['weekday', 'hour', 'engagement']])
    else:
        st.sidebar.write("No data for posting times yet.")

if __name__ == "__main__":
    main()
