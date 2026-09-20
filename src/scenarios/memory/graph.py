from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from src.schemas.state import AgentState
from src.scenarios.memory.nodes import trim_history

workflow = StateGraph(AgentState)
workflow.add_node("trim_history", trim_history)

workflow.add_conditional_edges(
    START,
    lambda state: "msgs >= 20" if len(state["messages"]) >= 20 else "msgs < 20",
    {
        "msgs >= 20": "trim_history",
        "msgs < 20": END,
	}
)
workflow.add_edge("trim_history", END)

def get_memory_graph() -> CompiledStateGraph:
    return workflow.compile()  


