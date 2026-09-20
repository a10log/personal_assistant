from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.routers import route_mode
from src.nodes import classify_scenario
from src.scenarios.tasks.graph import get_tasks_graph
from src.scenarios.memory.graph import get_memory_graph
from src.schemas.constants import ScenarioType
from src.schemas.state import AgentState

workflow = StateGraph(AgentState)
workflow.add_node("classify_scenario", classify_scenario)
workflow.add_node("scenario_tasks", get_tasks_graph())
workflow.add_node("manage_memory", get_memory_graph())

workflow.add_conditional_edges(
    START,
    route_mode,
    {
        "manage_memory": "manage_memory",
        "chat": "classify_scenario",
    },
)

workflow.add_conditional_edges(
    "classify_scenario",
    lambda state: state["scenario_type"],
    {
        ScenarioType.TASKS: "scenario_tasks",
        ScenarioType.DISCUSSION: END,
	}
)
workflow.add_edge("scenario_tasks", END)
workflow.add_edge("manage_memory", END)

def get_graph(checkpointer) -> CompiledStateGraph:
    return workflow.compile(checkpointer=checkpointer, debug=True)
   
