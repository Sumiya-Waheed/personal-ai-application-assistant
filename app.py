"""Streamlit entry point. UI wiring only."""
from __future__ import annotations
import streamlit as st
from config import APP_NAME, TOP_K
from rag.embeddings import EmbeddingService
from rag.retriever import Retriever
from llm.groq_client import GroqClient
from profile.profile_manager import ProfileManager
from ui import dashboard, profile_page, opportunity_page, match_page, assistant_page, resume_page

st.set_page_config(page_title=APP_NAME, page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

CUSTOM_CSS = """
<style>
:root { --accent:#5b5bd6; --muted:#667085; --card:#ffffff; }
.block-container { max-width: 1180px; padding-top: 2rem; }
.hero { padding: 1.4rem 1.5rem; border:1px solid rgba(91,91,214,.15); border-radius:18px;
        background:linear-gradient(135deg,rgba(91,91,214,.10),rgba(255,255,255,.92)); margin-bottom:1rem; }
.hero h1 { margin-bottom:.25rem; }
.small-muted { color:#667085; font-size:.9rem; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

@st.cache_resource(show_spinner="Loading the embedding model…")
def get_embeddings():
    return EmbeddingService()

def init_state():
    if "profile_manager" not in st.session_state:
        embeddings = get_embeddings()
        st.session_state.profile_manager = ProfileManager(embeddings)
        st.session_state.retriever = Retriever(st.session_state.profile_manager.store, embeddings)
    if "llm" not in st.session_state:
        try:
            st.session_state.llm = GroqClient()
        except Exception as exc:
            st.session_state.llm = None
            st.session_state.llm_error = str(exc)
    for key, default in {
        "profile_docs": [], "profile_files": [], "opportunity_text": None,
        "opportunity_analysis": None, "match_result": None, "resume": None,
        "resume_evidence": [], "chat_history": []
    }.items():
        st.session_state.setdefault(key, default)

init_state()

with st.sidebar:
    st.markdown("## 🎯 Personal AI Assistant")
    st.caption("Evidence-grounded application intelligence")
    if st.session_state.get("llm") is None:
        st.error("Groq API key not configured.")
        st.caption("Set GROQ_API_KEY locally or in Streamlit Cloud Secrets.")
    st.divider()
    page = st.radio("Navigate", ["Dashboard","My Profile","Opportunity","Match Analysis","Application Assistant","Resume"], index=0)
    st.divider()
    st.caption(f"Retrieval top-k: {TOP_K}")
    st.caption("Your profile is session-scoped in this MVP.")

state = st.session_state
if page == "Dashboard":
    dashboard.render(state)
elif page == "My Profile":
    profile_page.render(state)
elif page == "Opportunity":
    opportunity_page.render(state)
elif page == "Match Analysis":
    match_page.render(state)
elif page == "Application Assistant":
    assistant_page.render(state)
elif page == "Resume":
    resume_page.render(state)
