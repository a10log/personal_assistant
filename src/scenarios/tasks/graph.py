from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.scenarios.tasks.nodes import (
    call_function,
    call_llm_with_tools,
    check_need_call_function,
)
from src.schemas.state import AgentState

workflow = StateGraph(AgentState)

workflow.add_node("call_llm", call_llm_with_tools)
workflow.add_node("check_need_call_function", check_need_call_function)
workflow.add_node("call_function", call_function)

workflow.add_edge(START, "call_llm")
workflow.add_edge("call_llm", "check_need_call_function")
workflow.add_conditional_edges(
    "check_need_call_function",
    lambda state: state["need_call_function"],
    {
        True: "call_function",
        False: END,
    },
)
workflow.add_edge("call_function", "call_llm") 

def get_tasks_graph() -> CompiledStateGraph:
    return workflow.compile()  


