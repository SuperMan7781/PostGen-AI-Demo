import streamlit as st
import os
import sys

# 1. Setup paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from retrieval.search import VectorSearch
from generation.generation import generate_viral_post

# 2. App Configuration
st.set_page_config(page_title="PostGen AI", page_icon="🚀", layout="centered")

st.title("🚀 PostGen AI: The Viral LinkedIn Creator")
st.markdown("Generate high-performing LinkedIn posts based on real viral data.")

# 3. Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Settings")
    topic = st.text_input("Topic", placeholder="e.g., Remote Work")
    generate_btn = st.button("✨ Generate Post", type="primary")

# 4. Main App Logic
if generate_btn and topic:
    with st.spinner("🔎 Searching for viral inspiration..."):
        try:
            searcher = VectorSearch()
            viral_examples = searcher.search(topic, limit=3)
        except Exception as e:
            st.error(f"Search Error: {e}")
            viral_examples = []
    
    # Show what we found
    if viral_examples:
        with st.expander(f"✅ Found {len(viral_examples)} Viral Examples (Click to view)"):
            for i, ex in enumerate(viral_examples):
                st.markdown(f"**Example {i+1}** (Match: {ex.get('score', 0):.2f} | 👍 {ex['reactions']})")
                st.caption(f"{ex['text'][:150]}...")
                st.divider()
    else:
        st.info("⚠️ No exact matches found. Writing from scratch!")

    # Generate content
    with st.spinner("🧠 AI is analyzing patterns and writing..."):
        try:
            final_post = generate_viral_post(topic, viral_examples)
            
            st.success("✨ Your Viral Post is Ready!")
            st.text_area("Copy this:", value=final_post, height=300)
            
        except Exception as e:
            st.error(f"Generation Error: {e}")

elif generate_btn and not topic:
    st.warning("⚠️ Please enter a topic first!")

# Footer
st.markdown("---")
st.caption("Powered by Gemini 2.5 Flash & Qdrant Vector Search")