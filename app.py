import streamlit as st
import fitz  # PyMuPDF
from google import genai

# --- 1. SETUP ---
st.set_page_config(page_title="Nyaya AI 2026", page_icon="⚖️")
st.title("⚖️ Supreme Court Summarizer")

# --- 2. AI CONFIG ---
# Paste your API Key here
API_KEY = "AIzaSyBFP4Ek-xX9Wt4ujuf4liLhZYy_9HFsjKY" 
client = genai.Client(api_key=API_KEY)

# --- 3. SESSION STATE ---
if "summary" not in st.session_state:
    st.session_state.summary = ""

# --- 4. UPLOADER ---
file = st.file_uploader("Upload Judgment (PDF)", type=['pdf'])

if file:
    if st.button("⚖️ Generate AI Summary"):
        with st.spinner("Analyzing document with Gemini 2.0..."):
            try:
                # Extract text
                doc = fitz.open(stream=file.read(), filetype="pdf")
                text = "".join([page.get_text() for page in doc])
                
                # Send to the most stable 2026 model
                response = client.models.generate_content(
                    model='gemini-2.0-flash', 
                    contents=f"Provide a legal summary of this judgment including: 1. Case Name, 2. Key Facts, 3. Legal Issues, 4. Final Decision. Text: {text[:25000]}"
                )
                st.session_state.summary = response.text
                st.success("Summary Generated!")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# --- 5. DISPLAY & DOWNLOAD ---
if st.session_state.summary:
    st.markdown("---")
    st.markdown(st.session_state.summary)
    st.download_button(
        label="📥 Download Summary",
        data=st.session_state.summary,
        file_name="legal_summary.txt",
        mime="text/plain"
    )
