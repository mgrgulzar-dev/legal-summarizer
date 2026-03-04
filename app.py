import streamlit as st
import fitz  # PyMuPDF
from google import genai

# --- 1. SETUP ---
st.set_page_config(page_title="Nyaya AI 2026", page_icon="⚖️")
st.title("⚖️ Supreme Court Summarizer")

# --- 2. AI CONFIG (2026 Stable) ---
# Replace with your key
API_KEY = "AIzaSyBFP4Ek-xX9Wt4ujuf4liLhZYy_9HFsjKY" 
client = genai.Client(api_key=API_KEY)

# --- 3. UPLOADER ---
file = st.file_uploader("Upload Judgment (PDF)", type=['pdf'])

if file:
    # Use a session state to avoid re-running extraction every click
    if 'extracted_text' not in st.session_state:
        with st.spinner("Extracting Legal Text..."):
            doc = fitz.open(stream=file.read(), filetype="pdf")
            text = "".join([page.get_text() for page in doc])
            st.session_state.extracted_text = text[:30000]

    if st.button("⚖️ Generate AI Summary"):
        with st.spinner("Analyzing with Gemini 2.5..."):
            try:
                # Using the current 2026 stable alias
                response = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=f"Summarize this Indian Court judgment: {st.session_state.extracted_text}"
                )
                st.markdown("### 📌 Case Summary")
                st.write(response.text)
                st.success("Analysis Complete!")
            except Exception as e:
                st.error(f"AI Error: {e}")