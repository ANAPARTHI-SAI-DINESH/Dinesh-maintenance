"""Streamlit web UI for the maintenance agent.

Run with:  streamlit run app.py
A simple screen: type a fault, the agent resolves it, and if it drafted a
purchase order you approve or reject it with a button (the human-in-the-loop gate).
"""
import json

import streamlit as st
from langchain_core.messages import HumanMessage

from src import db, rag
from src.agent import build_agent

st.set_page_config(page_title="Maintenance Agent", page_icon="🔧")
st.title("🔧 Maintenance Resolution Agent")


@st.cache_resource
def _setup():
    """Set up DB + manual index + agent once (cached across reruns)."""
    db.init_db()
    rag.build_index()
    return build_agent()


agent = _setup()

fault = st.text_input("Describe the fault", "Machine CNC-7 threw fault E-214")

if st.button("Diagnose"):
    with st.spinner("Agent working..."):
        result = agent.invoke({"messages": [HumanMessage(content=fault)]})
    st.session_state["summary"] = result["messages"][-1].content
    po = None
    for m in reversed(result["messages"]):
        if getattr(m, "name", None) == "draft_purchase_order":
            try:
                po = json.loads(m.content)
            except (ValueError, TypeError):
                po = None
            break
    st.session_state["po"] = po

if "summary" in st.session_state:
    st.subheader("Resolution")
    st.write(st.session_state["summary"])

    po = st.session_state.get("po")
    if po:
        st.warning("A purchase order needs your approval:")
        st.json(po)
        c1, c2 = st.columns(2)
        if c1.button("✅ Approve & submit"):
            db.save_purchase_order(json.dumps(po), "SUBMITTED")
            st.success("Purchase order submitted.")
        if c2.button("❌ Reject"):
            db.save_purchase_order(json.dumps(po), "REJECTED")
            st.error("Purchase order rejected.")
