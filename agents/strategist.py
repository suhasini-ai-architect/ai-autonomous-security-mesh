import requests
import json

def strategist_node(state):
    print("--- 🧠 STRATEGIST AGENT MAPPING MITIGATION ---")
    
    # We pass the forensic report into the prompt
    prompt = f"""
    You are a Senior Security Architect. 
    Based on this Forensic Report: {state['analysis_report']}
    
    Design a 2-step mitigation plan:
    1. IMMEDIATE_ACTION: (e.g., Block IP, Kill Process)
    2. LONG_TERM_PATCH: (e.g., Update Firewall, Rotate Keys)
    
    Be concise. Output the steps as a bulleted list.
    """
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }
    )
    
    result = response.json()['response']
    
    # We split the result into a list for the state
    steps = result.strip().split('\n')
    
    return {
        "mitigation_plan": steps,
        "audit_trail": ["Strategist Agent finalized the mitigation roadmap."]
    }