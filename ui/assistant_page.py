import streamlit as st
from features.application_assistant import ApplicationAssistant
from features.evidence import source_labels

def render(state):
    st.title("Application Assistant")
    if not state.get("opportunity_text"):
        st.info("Analyze an opportunity first.")
        return
    if not state.get("profile_manager") or state["profile_manager"].store.is_empty:
        st.info("Build your personal knowledge base first.")
        return
    if "chat_history" not in state: state["chat_history"] = []
    for msg in state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                st.caption("Evidence used")
                for src in msg["sources"]: st.write(f"- {src}")
    question = st.chat_input("Ask an application question…")
    if question:
        state["chat_history"].append({"role":"user","content":question})
        with st.chat_message("user"): st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Retrieving profile evidence…"):
                try:
                    assistant = ApplicationAssistant(state["llm"], state["retriever"])
                    answer, evidence = assistant.answer(question, state["opportunity_text"])
                    st.markdown(answer)
                    sources = source_labels(evidence)
                    st.caption("Evidence used")
                    for src in sources: st.write(f"- {src}")
                    state["chat_history"].append({"role":"assistant","content":answer,"sources":sources})
                except Exception as exc:
                    st.error(str(exc))
    if state.get("chat_history"):
        st.markdown("### Refine the latest answer")
        last = next((m for m in reversed(state["chat_history"]) if m["role"]=="assistant"), None)
        if last:
            cols = st.columns(4)
            instructions = [("Shorter","Make this answer more concise."),("Formal","Make this answer more formal."),("Personal","Make this answer more personal without adding facts."),("Clearer","Improve clarity without adding facts.")]
            for col, (label, instruction) in zip(cols, instructions):
                if col.button(label):
                    with st.spinner("Refining…"):
                        try:
                            assistant = ApplicationAssistant(state["llm"], state["retriever"])
                            answer, evidence = assistant.refine(last["content"], instruction)
                            sources = source_labels(evidence)
                            state["chat_history"].append({"role":"assistant","content":answer,"sources":sources})
                            st.rerun()
                        except Exception as exc:
                            st.error(str(exc))
