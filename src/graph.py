# graph.py
from langgraph.graph import START, END, StateGraph
from src.nodes.call_llm import call_llm_with_tools
from src.nodes.call_function import call_function
from src.nodes.router import route_after_call_llm
from src.schemas.state import AgentState

workflow = StateGraph(AgentState)

workflow.add_node("call_llm_with_tools", call_llm_with_tools)
workflow.add_node("call_function", call_function)

workflow.add_edge(START, "call_llm_with_tools")


workflow.add_conditional_edges(
    "call_llm_with_tools",
    route_after_call_llm,
    {
        "call_function": "call_function",
        "end": END,
    },
)

workflow.add_edge("call_function", "call_llm_with_tools")


def get_graph(checkpointer):
    return workflow.compile(checkpointer=checkpointer, debug=True)
