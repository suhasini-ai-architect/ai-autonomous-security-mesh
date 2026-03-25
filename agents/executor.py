def executor_node(state):
    print("--- 🛠️ EXECUTOR AGENT APPLYING PATCHES ---")
    
    plan = state['mitigation_plan']
    
    # In a real 1.8 Cr scenario, this would call an Azure SDK or Ansible.
    # Here, we simulate the 'Self-Healing' execution.
    execution_log = f"Executed actions: {', '.join(plan[:2])}"
    
    # We simulate a 80% success rate to trigger the 'Self-Healing' loop occasionally
    import random
    success = random.random() > 0.2 
    
    return {
        "action_result": execution_log,
        "is_resolved": success,
        "audit_trail": [f"Executor attempted actions. Success: {success}"]
    }