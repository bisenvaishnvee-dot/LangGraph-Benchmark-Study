from langgraph.graph import END, START, StateGraph

from src.nodes import answer_node, coding_node, router_node, verification_node
from src.state import AgentState


def choose_agent(state: AgentState) -> str:
    return "coding" if state.get("route") == "coding" else "answer"


def build_graph():
    """Build and compile the explicit LangGraph workflow."""
    workflow = StateGraph(AgentState)
    workflow.add_node("router", router_node)
    workflow.add_node("answer", answer_node)
    workflow.add_node("coding", coding_node)
    workflow.add_node("verification", verification_node)

    workflow.add_edge(START, "router")
    workflow.add_conditional_edges(
        "router",
        choose_agent,
        {"coding": "coding", "answer": "answer"},
    )
    workflow.add_edge("answer", "verification")
    workflow.add_edge("coding", "verification")
    workflow.add_edge("verification", END)
    return workflow.compile()
