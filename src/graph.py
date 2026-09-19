from langgraph.graph import START, END, MessagesState, StateGraph
from src.nodes.call_llm import call_llm

workflow = StateGraph(MessagesState)
workflow.add_node("call_llm", call_llm)
workflow.add_edge(START, "call_llm")
workflow.add_edge("call_llm", END)

def compile_graph(checkpointer):
	return workflow.compile(checkpointer=checkpointer)