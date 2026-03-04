import streamlit as st
import fitz  # PyMuPDF
from google import genai

# --- 1. SETUP ---
st.set_page_config(page_title="Nyaya AI", page_icon="⚖️")
st.title("⚖️ Supreme Court Summarizer")

# AI CONFIG
API_KEY = "AIzaSyBFP4Ek-xX9Wt4ujuf4liLhZYy_9HFsjKY" 
client = genai.Client(api_key=API_KEY)

# --- 2. SESSION STATE (The Download Fix) ---
if "summary" not in st.session_state:
    st.session_state.summary = ""

# --- 3. UPLOADER ---
file = st.file_uploader("Upload Judgment (PDF)", type=['pdf'])

if file:
    # Use a spinner so the user knows it's working
    if st.button("⚖️ Generate AI Summary"):
        with st.spinner("Analyzing legal document..."):
            doc = fitz.open(stream=file.read(), filetype="pdf")
            text = "".join([page.get_text() for page in doc])
            
            # Send to AI
            response = client.models.generate_content(
                model='gemini-2.0-flash', # Stable 2026 model
                contents=f"Summarize this Indian Court judgment with Case Name, Facts, Issues, and Ratio Decidendi: {text[:25000]}"
            )
            # SAVE TO SESSION STATE
            st.session_state.summary = response.text

# --- 4. DISPLAY & DOWNLOAD ---
if st.session_state.summary:
    st.markdown("---")
    st.subheader("📌 Case Summary")
    st.write(st.session_state.summary)
    
    # This button now works because the data is saved in session_state
    st.download_button(
        label="📥 Download Summary as Text",
        data=st.session_state.summary,
        file_name="judgment_summary.txt",
        mime="text/plain"
    )
