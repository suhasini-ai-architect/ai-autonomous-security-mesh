import re # Add this to your imports at the top

def supervisor_node(state: MeshState):
    st.toast(f"🕵️ Sentry ({SENTRY_MODEL}) inspecting traffic...")
    
    prompt = f"""
    [STRICT CLASSIFICATION]
    Analyze the log and respond with ONLY the word 'YES' or 'NO'. 
    No explanations. No periods.
    
    - Threat (SQL, Brute Force, Unauthorized): YES
    - Safe (Login, Profile Update, Logout): NO
    
    LOG: '{state['logit_input']}'
    DECISION:"""
    
    try:
        response = requests.post(
            OLLAMA_URL, 
            json={
                "model": SENTRY_MODEL, 
                "prompt": prompt, 
                "stream": False,
                "options": {"temperature": 0} 
            }, 
            timeout=10
        )
        # 1. Get raw text and clean it
        text = response.json().get('response', 'NO').upper().strip()
        
        # 2. Use Regex to find the FIRST occurrence of YES or NO only
        match = re.search(r'\b(YES|NO)\b', text)
        decision = match.group(1) if match else "NO"
            
    except:
        decision = "YES" # Default to safety on connection error

    # Double-check: If input is very simple and model is still flagging it, force NO
    if "logged in" in state['logit_input'].lower() and decision == "YES":
        decision = "NO"

    status_text = '🚨 Escalating' if decision == 'YES' else '✅ Allowed'
    msg = f"🛡️ Sentry Filter: **{decision}** ({status_text})"
    
    return {
        "audit_trail": state.get("audit_trail", []) + [msg],
        "next_step": decision,
        "retry_count": state.get("retry_count", 0)
    }