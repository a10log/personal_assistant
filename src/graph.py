from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from src.schemas.state import AgentState
from src.scenarios.nodes import classify_scenario



from src.nodes.call_llm import call_llm_with_tools
from src.nodes.call_function import call_function
from src.nodes.router import route_after_call_llm

from src.utils.docs import save_graph_image

workflow = StateGraph(AgentState)
workflow.add_node("classify_scenario", classify_scenario)
workflow.add_edge(START, "classify_scenario")
workflow.add_edge("classify_scenario", END)




# workflow.add_node("call_llm_with_tools", call_llm_with_tools)
# workflow.add_node("call_function", call_function)

# workflow.add_edge(START, "call_llm_with_tools")

# workflow.add_conditional_edges(
#     "call_llm_with_tools",
#     route_after_call_llm,
#     {
#         "call_function": "call_function",
#         "end": END,
#     },
# )

# workflow.add_edge("call_function", "call_llm_with_tools")

def get_graph(checkpointer) -> CompiledStateGraph:
    graph = workflow.compile(checkpointer=checkpointer, debug=True)
    save_graph_image(graph)
    return graph
