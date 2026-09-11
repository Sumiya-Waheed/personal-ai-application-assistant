import streamlit as st
from opportunity.matcher import OpportunityMatcher
from features.readiness_score import calculate_readiness

def render(state):
    st.title("Match Analysis")
    if not state.get("opportunity_analysis"):
        st.info("Analyze an opportunity first.")
        return
    if not state.get("profile_manager") or state["profile_manager"].store.is_empty:
        st.info("Build your personal knowledge base first.")
        return
    if st.button("Run profile ↔ opportunity match", type="primary"):
        with st.spinner("Retrieving evidence and comparing requirements…"):
            try:
                retriever = state["retriever"]
                matcher = OpportunityMatcher(state["llm"], retriever)
                evidence = matcher.retrieve_for_analysis(state["opportunity_analysis"])
                result = matcher.match(state["opportunity_analysis"], evidence)
                score, category_scores = calculate_readiness(result)
                result["_evidence"] = evidence
                result["_readiness"] = score
                result["_category_scores"] = category_scores
                state["match_result"] = result
            except Exception as exc:
                st.error(str(exc))
    result = state.get("match_result")
    if not result: return
    score = result["_readiness"]
    st.markdown("### Application Readiness")
    st.metric("AI-generated profile match/readiness estimate", f"{score}%")
    st.caption("This is an AI-assisted estimate based on extracted requirements and retrieved evidence; it is not a scientifically validated probability.")
    st.progress(score / 100)
    st.markdown("#### Category breakdown")
    cols = st.columns(5)
    names = [("Eligibility","eligibility"),("Skills","skills"),("Experience","experience"),("Documents","documents"),("Other","other")]
    for col, (label, key) in zip(cols, names):
        col.metric(label, f"{result['_category_scores'][key]}%")
    for title, key, icon in [("Matches","matches","✓"),("Gaps / missing information","gaps","⚠"),("Unclear","unclear","?")]:
        st.markdown(f"### {icon} {title}")
        items = result.get(key, [])
        if items:
            for item in items: st.write(f"- {item}")
        else:
            st.write("None identified.")
    st.markdown("### Evidence")
    for item in result.get("_evidence", []):
        with st.expander(f"{item['source']} · {item.get('section') or 'Relevant excerpt'} · similarity {item['score']:.2f}"):
            st.write(item["text"])
