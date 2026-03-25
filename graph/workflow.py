from langgraph.graph import StateGraph, END
from .state import AgentState
from agents.forensic_agent import forensic_node
from agents.strategist import strategist_node
from agents.executor import executor_node
from agents.supervisor import supervisor_node

# 1. Routing Logic Functions
def supervisor_gate(state: AgentState):
    """Decides whether to investigate or ignore based on Supervisor output."""
    last_message = state["audit_trail"][-1].upper()
    if "YES" in last_message:
        return "investigate"
    return "ignore"

def check_remediation(state: AgentState):
    """Routes based on whether the Executor successfully patched the threat."""
    if state["is_resolved"]:
        return "end"
    elif state.get("retry_count", 0) >= 3:
        return "end"
    else:
        return "retry"

# 2. Build the Graph
workflow = StateGraph(AgentState)

# Add all Nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("forensics", forensic_node)
workflow.add_node("strategist", strategist_node)
workflow.add_node("executor", executor_node)

# 3. Define the Orchestration Flow
workflow.set_entry_point("supervisor")

# Conditional Edge 1: Supervisor -> (Forensics OR End)
workflow.add_conditional_edges(
    "supervisor",
    supervisor_gate,
    {
        "investigate": "forensics",
        "ignore": END
    }
)

# Standard Edges
workflow.add_edge("forensics", "strategist")
workflow.add_edge("strategist", "executor")

# Conditional Edge 2: Executor -> (Strategist OR End)
workflow.add_conditional_edges(
    "executor",
    check_remediation,
    {
        "retry": "strategist",
        "end": END
    }
)

# 4. Compile
app = workflow.compile()