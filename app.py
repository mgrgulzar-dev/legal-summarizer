import streamlit as st
import fitz  # PyMuPDF
from google import genai
from google.genai import errors

# --- 1. SETUP ---
st.set_page_config(page_title="Nyaya AI 2026", page_icon="⚖️")
st.title("⚖️ Supreme Court Summarizer")

# --- 2. AI CONFIG ---
API_KEY = "AIzaSyBa1kqdg3yjKyEojjUFD9LHz2k0IUE1_WA" # Replace this!
client = genai.Client(api_key=API_KEY)

# --- 3. SESSION STATE ---
if "summary" not in st.session_state:
    st.session_state.summary = ""

# --- 4. UPLOADER ---
file = st.file_uploader("Upload Judgment (PDF)", type=['pdf'])

if file:
    if st.button("⚖️ Generate AI Summary"):
        with st.spinner("Analyzing document..."):
            try:
                # Extract text
                doc = fitz.open(stream=file.read(), filetype="pdf")
                text = "".join([page.get_text() for page in doc])
                
                # Using the 2026 'Stable' alias to avoid 403/404 errors
                response = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=f"Summarize this Indian judgment: {text[:20000]}"
                )
                st.session_state.summary = response.text
                st.success("Summary Generated!")
            except errors.ClientError as e:
                st.error(f"Permission Error (403): Please check if your API Key is active in Google AI Studio and that you are in a supported region.")
            except Exception as e:
                st.error(f"Error: {e}")

# --- 5. DISPLAY & DOWNLOAD ---
if st.session_state.summary:
    st.markdown("---")
    st.markdown(st.session_state.summary)
    st.download_button("📥 Download Summary", st.session_state.summary, "summary.txt")
