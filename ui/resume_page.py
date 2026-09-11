import streamlit as st
from features.resume_generator import ResumeGenerator
from features.evidence import source_labels

def render(state):
    st.title("Tailored Resume")
    if not state.get("opportunity_text"):
        st.info("Analyze an opportunity first.")
        return
    if not state.get("profile_manager") or state["profile_manager"].store.is_empty:
        st.info("Build your personal knowledge base first.")
        return
    if st.button("Generate Tailored Resume", type="primary"):
        with st.spinner("Selecting relevant evidence and drafting your resume…"):
            try:
                generator = ResumeGenerator(state["llm"], state["retriever"])
                resume, evidence = generator.generate(state["opportunity_text"])
                state["resume"] = resume
                state["resume_evidence"] = evidence
            except Exception as exc:
                st.error(str(exc))
    if state.get("resume"):
        st.markdown("### Resume preview")
        st.markdown(state["resume"])
        st.download_button("Download Markdown", state["resume"], file_name="tailored_resume.md", mime="text/markdown")
        st.markdown("### Evidence used")
        for src in source_labels(state.get("resume_evidence", [])):
            st.write(f"- {src}")
