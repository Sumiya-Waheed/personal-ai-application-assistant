import streamlit as st
from utils.file_parser import extract_text
from utils.validators import validate_upload
from opportunity.analyzer import OpportunityAnalyzer

def render(state):
    st.title("Opportunity")
    st.write("Upload a scholarship, job, internship, fellowship, or university-program description.")
    upload = st.file_uploader("Opportunity document", type=["pdf", "docx", "txt"], key="opportunity_uploader")
    if upload:
        ok, msg = validate_upload(upload.name, upload.size)
        if not ok:
            st.error(msg); return
        if st.button("Analyze Opportunity", type="primary"):
            with st.spinner("Reading the opportunity and extracting explicit requirements…"):
                try:
                    text = extract_text(upload.name, upload.getvalue())
                    state["opportunity_text"] = text
                    state["opportunity_analysis"] = OpportunityAnalyzer(state["llm"]).analyze(text)
                    state["match_result"] = None
                    st.success("Opportunity analyzed.")
                except Exception as exc:
                    st.error(str(exc))
    analysis = state.get("opportunity_analysis")
    if analysis:
        st.markdown("### Opportunity intelligence")
        labels = [
            ("Opportunity type","opportunity_type"),("Eligibility","eligibility_requirements"),
            ("Education","education_requirements"),("Required skills","required_skills"),
            ("Required experience","required_experience"),("Preferred qualifications","preferred_qualifications"),
            ("Documents required","documents_required"),("Important criteria","important_criteria"),
            ("Application questions","application_questions"),("Other requirements","other_requirements")
        ]
        for title, key in labels:
            value = analysis.get(key, [])
            if value:
                st.markdown(f"**{title}**")
                if isinstance(value, list):
                    for item in value: st.markdown(f"- {item}")
                else:
                    st.write(value)
