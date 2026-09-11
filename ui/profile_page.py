import streamlit as st
from utils.validators import validate_upload

def render(state):
    st.title("My Profile")
    st.write("Upload personal profile documents. These are kept in the current app session and are never treated as opportunity content.")
    st.caption("Supported: PDF, DOCX, TXT. Maximum upload size is configured in the app.")
    uploads = st.file_uploader(
        "Personal profile documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="profile_uploader",
        help="Examples: CV, certificates, project descriptions, awards, volunteering, leadership, experience, skills."
    )
    if uploads:
        bad = []
        for f in uploads:
            ok, msg = validate_upload(f.name, f.size)
            if not ok: bad.append(msg)
        if bad:
            for msg in bad: st.error(msg)
        elif st.button("Build personal knowledge base", type="primary"):
            with st.spinner("Extracting, chunking and indexing your documents…"):
                try:
                    docs = state["profile_manager"].rebuild(uploads)
                    state["profile_docs"] = docs
                    state["profile_files"] = [f.name for f in uploads]
                    state["match_result"] = None
                    st.success(f"Knowledge base ready: {len(docs)} document(s), {len(state['profile_manager'].store.records)} evidence chunks.")
                except Exception as exc:
                    st.error(str(exc))
    if state.get("profile_docs"):
        st.markdown("### Current profile sources")
        for doc in state["profile_docs"]:
            st.write(f"**{doc.filename}** · {doc.document_type} · {doc.chunks} chunks")
