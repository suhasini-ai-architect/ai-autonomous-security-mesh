import requests
import json
from graph.state import AgentState

def forensic_node(state: AgentState):
    print("--- 🔍 FORENSIC AGENT ANALYZING LOGS ---")
    
    prompt = f"""
    You are an Expert Cyber Forensic Analyst. 
    Analyze these logs: {state['raw_logs']}
    Identify:
    1. Attack Type
    2. Severity (Low/Medium/High)
    3. Source of Threat
    
    Output your findings clearly.
    """
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            }
        )
        result = response.json()['response']
    except Exception as e:
        result = f"Error connecting to Ollama: {str(e)}"
    
    return {
        "analysis_report": result,
        "audit_trail": ["Forensic Agent completed threat analysis."]
    }