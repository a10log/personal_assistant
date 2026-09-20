from langgraph.graph import START, END, StateGraph
from src.nodes.call_llm import call_llm
from src.schemas.state import AgentState

workflow = StateGraph(AgentState)
workflow.add_node("call_llm", call_llm)
workflow.add_edge(START, "call_llm")
workflow.add_edge("call_llm", END)

def get_graph(checkpointer):
	return workflow.compile(checkpointer=checkpointer, debug=True)