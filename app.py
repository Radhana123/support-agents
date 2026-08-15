import streamlit as st
import sys
sys.path.append("src")

from orchestrator import handle_query
from ticket_store import get_all_tickets, get_escalated_tickets

st.set_page_config(page_title="Support Agent", layout="wide")

st.title("Autonomous Customer Support Agent")

tab1, tab2 = st.tabs(["Chat", "Escalation Dashboard"])

with tab1:
    st.write("Ask a question about FastAPI (this demo's knowledge base)")

    query = st.text_input("Your question")

    if st.button("Send") and query:
        with st.spinner("Processing..."):
            result = handle_query(query)

        st.divider()

        col1, col2, col3 = st.columns(3)
        col1.metric("Category", result["classification"]["category"])
        col2.metric("Urgency", result["classification"]["urgency"])
        col3.metric("Status", result["status"])

        if result["status"] == "auto_resolved":
            st.success("Answer (High Confidence)")
        else:
            st.warning("Escalated to Human (Low/Medium Confidence)")

        st.write(result["answer"])

        with st.expander("Sources used"):
            for src in result["sources"]:
                st.write("- " + src)

with tab2:
    st.subheader("Escalated Tickets")

    escalated = get_escalated_tickets()

    if not escalated:
        st.info("No escalated tickets yet.")
    else:
        for ticket in escalated:
            with st.container():
                st.write("**Query:** " + ticket[1])
                st.write("Category: " + ticket[2] + " | Urgency: " + ticket[3] + " | Confidence: " + ticket[5])
                st.write("Answer given: " + ticket[4])
                st.caption("Logged at: " + ticket[7])
                st.divider()

    st.subheader("All Tickets")
    all_tickets = get_all_tickets()
    st.write("Total tickets: " + str(len(all_tickets)))