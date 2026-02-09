import sys
import requests
import streamlit as st

from core import StockSageException

BASE_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="StockSage AI",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .bot-message {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 StockSage AI")
st.caption("Your intelligent stock market assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar: Document Upload
with st.sidebar:
    st.header("📄 Knowledge Base")
    st.markdown("Upload stock market PDFs or DOCX files to enhance the AI's knowledge.")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Upload documents about trading strategies, market analysis, etc."
    )
    
    if st.button("📤 Upload & Process", use_container_width=True):
        if uploaded_files:
            files = []
            for f in uploaded_files:
                file_data = f.read()
                if file_data:
                    files.append(("files", (f.name, file_data, f.type)))
            
            if files:
                try:
                    with st.spinner("Processing documents..."):
                        response = requests.post(f"{BASE_URL}/upload", files=files)
                        
                    if response.status_code == 200:
                        st.success("✅ Documents processed successfully!")
                    else:
                        st.error(f"❌ Error: {response.text}")
                except requests.ConnectionError:
                    st.error("❌ Cannot connect to backend. Is the server running?")
                except Exception as e:
                    raise StockSageException(e, sys)
            else:
                st.warning("⚠️ Files appear to be empty.")
        else:
            st.warning("⚠️ Please select files first.")
    
    st.divider()
    st.markdown("### 🔧 Settings")
    st.caption(f"Backend: `{BASE_URL}`")

# Display chat history
st.header("💬 Chat")

for chat in st.session_state.messages:
    if chat["role"] == "user":
        with st.chat_message("user"):
            st.write(chat["content"])
    else:
        with st.chat_message("assistant"):
            st.write(chat["content"])

# Chat input
if prompt := st.chat_input("Ask about stocks, trading strategies, market analysis..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    f"{BASE_URL}/query",
                    json={"question": prompt},
                    timeout=60
                )
                
                if response.status_code == 200:
                    answer = response.json().get("answer", "No response received.")
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = f"Error: {response.text}"
                    st.error(error_msg)
                    
            except requests.ConnectionError:
                st.error("❌ Cannot connect to backend. Please ensure the server is running.")
            except requests.Timeout:
                st.error("❌ Request timed out. The query may be too complex.")
            except Exception as e:
                raise StockSageException(e, sys)
