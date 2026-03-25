import streamlit as st
from graph.workflow import app
import time

# --- Page Config ---
st.set_page_config(page_title="Autonomous Security Mesh", layout="wide")

st.title("🛡️ Autonomous AI Security & Self-Healing Mesh")
st.markdown("""
    **Senior Architect Demo:** This system uses a Multi-Agent LangGraph workflow to 
    Detect, Analyze, and Remediate security threats locally using **Llama-3.2-3B**.
""")

# --- Sidebar: Configuration & Simulation ---
with st.sidebar:
    st.header("Simulation Settings")
    model_choice = st.selectbox("LLM Backbone", ["Llama-3.2-3B (Local)"])
    
    st.subheader("Inject Mock Security Log")
    sample_logs = {
        "Brute Force": "Multiple failed login attempts from IP 192.168.1.45 on port 22.",
        "SQL Injection": "Detected 'OR 1=1' pattern in query string from session_id: 8829.",
        "DDoS Warning": "Inbound traffic spike: 10,000 req/sec from geographically diverse IPs."
    }
    selected_sample = st.selectbox("Select Attack Scenario", list(sample_logs.keys()))
    user_input = st.text_area("Or enter custom log:", sample_logs[selected_sample])

# --- Main Interface ---
if st.button("🚀 Trigger Incident Response"):
    if user_input:
        # Initial State for LangGraph
        initial_state = {
            "raw_logs": user_input,
            "analysis_report": "",
            "mitigation_plan": [],
            "action_result": "",
            "is_resolved": False,
            "retry_count": 0,
            "audit_trail": [f"Incident triggered for: {selected_sample}"]
        }
        
        with st.status("Agents are collaborating...", expanded=True) as status:
            st.write("🔍 Forensic Agent identifying threat...")
            # Invoke the LangGraph app
            final_state = app.invoke(initial_state)
            status.update(label="Response Complete!", state="complete", expanded=False)

        # --- Display Results in Columns ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔬 Forensic Analysis")
            st.info(final_state.get("analysis_report", "No data"))
            
            st.subheader("🛠️ Mitigation Actions")
            for step in final_state.get("mitigation_plan", []):
                st.write(f"✅ {step}")

        with col2:
            st.subheader("⚖️ Resolution Status")
            if final_state["is_resolved"]:
                st.success("STATUS: REMEDIATED")
            else:
                st.error("STATUS: ESCALATED TO HUMAN")
            
            st.metric("Self-Healing Retries", final_state["retry_count"])
            
            st.subheader("📜 Audit Trail")
            for trail in final_state["audit_trail"]:
                st.caption(f"• {trail}")

    else:
        st.warning("Please enter a log to analyze.")