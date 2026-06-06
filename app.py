from dotenv import load_dotenv
import streamlit as st
import os
#from dotenv import load_dotenv
from pathlib import Path 
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)
from backend.agent import TravelAgent
from backend.database import init_db, save_search, get_search_history
from backend.rag import RAGChatbot

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Travel Concierge",
    page_icon="✈️",
    layout="wide",
)

# ── Init DB & session state ────────────────────────────────────────────────────
init_db()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = TravelAgent()
if "rag" not in st.session_state:
    st.session_state.rag = RAGChatbot()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("✈️ AI Travel Concierge")
    st.markdown("---")

    mode = st.radio("Mode", ["💬 Chat Agent", "📄 Document Q&A", "🕓 Search History"])

    if mode == "📄 Document Q&A":
        st.subheader("Upload Travel Documents")
        uploaded = st.file_uploader(
            "Upload PDF / TXT", type=["pdf", "txt"], accept_multiple_files=True
        )
        if uploaded:
            saved_paths = []
            for f in uploaded:
                path = os.path.join("data/uploads", f.name)
                with open(path, "wb") as out:
                    out.write(f.read())
                saved_paths.append(path)
            if st.button("Index Documents"):
                with st.spinner("Indexing…"):
                    st.session_state.rag.load_documents(saved_paths)
                st.success(f"Indexed {len(saved_paths)} document(s)!")

    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ── Main area ──────────────────────────────────────────────────────────────────
st.header("✈️ AI Travel Concierge")

# ── SEARCH HISTORY ─────────────────────────────────────────────────────────────
if mode == "🕓 Search History":
    st.subheader("Your Past Searches")
    history = get_search_history()
    if not history:
        st.info("No searches saved yet.")
    else:
        for row in history:
            with st.expander(f"🔍 {row['query'][:60]}  —  {row['created_at']}"):
                st.write(row["response"])
    st.stop()

# ── CHAT AREA ──────────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

placeholder = (
    "Ask me anything about travel – flights, hotels, weather, itineraries…"
    if mode == "💬 Chat Agent"
    else "Ask a question about your uploaded documents…"
)

if prompt := st.chat_input(placeholder):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            if mode == "📄 Document Q&A":
                response = st.session_state.rag.query(prompt)
            else:
                response = st.session_state.agent.run(prompt)

        st.markdown(response)
        save_search(prompt, response)

    st.session_state.messages.append({"role": "assistant", "content": response})
