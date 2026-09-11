import streamlit as st

def render(state):
    st.title("Personal AI Application Assistant")
    st.caption("One verified profile → many opportunities → evidence-grounded applications.")
    docs = state.get("profile_docs", [])
    analysis = state.get("opportunity_analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Profile documents", len(docs))
    col2.metric("Knowledge chunks", len(state.get("profile_manager").store.records) if state.get("profile_manager") else 0)
    col3.metric("Opportunity", "Ready" if analysis else "Not analyzed")
    st.markdown("### How it works")
    st.markdown("""
    1. **Build your profile** from your own CV, certificates, projects, and experience documents.
    2. **Upload an opportunity** and let the assistant extract its explicit requirements.
    3. **Match evidence** from your profile to the opportunity and surface gaps or uncertainty.
    4. **Generate grounded answers** with visible source evidence.
    5. **Tailor a resume** without inventing any personal claims.
    """)
    st.info("Privacy: documents are used for personalized assistance. Do not upload passwords, payment information, or other highly sensitive credentials.")
