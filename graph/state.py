from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    raw_logs: str
    analysis_report: str
    mitigation_plan: List[str]
    action_result: str
    is_resolved: bool
    retry_count: int
    audit_trail: Annotated[List[str], operator.add]