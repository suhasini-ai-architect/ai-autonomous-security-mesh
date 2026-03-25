import requests

def supervisor_node(state):
    print("--- 🛡️ SUPERVISOR AGENT EVALUATING INCIDENT ---")
    
    prompt = f"""
    You are a Security Operations Center (SOC) Supervisor.
    Determine if the following log requires a full forensic investigation:
    "{state['raw_logs']}"
    
    Respond with only 'YES' or 'NO'.
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
        decision = response.json()['response'].strip().upper()
    except:
        decision = "YES" # Default to safety
    
    return {
        "audit_trail": [f"Supervisor Decision: {decision}"],
        "retry_count": state.get("retry_count", 0)
    }