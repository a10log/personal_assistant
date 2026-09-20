from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.nodes import classify_scenario
from src.scenarios.tasks.graph import get_tasks_graph
from src.schemas.constants import ScenarioType
from src.schemas.state import AgentState
from src.utils.docs import save_graph_image

workflow = StateGraph(AgentState)
workflow.add_node("classify_scenario", classify_scenario)
workflow.add_node("scenario_tasks", get_tasks_graph())

workflow.add_edge(START, "classify_scenario")
workflow.add_conditional_edges(
    "classify_scenario",
    lambda state: state["scenario_type"],
    {
        ScenarioType.TASKS: "scenario_tasks",
        ScenarioType.DISCUSSION: END,
	}
)
workflow.add_edge("scenario_tasks", END)

def get_graph(checkpointer) -> CompiledStateGraph:
    graph = workflow.compile(checkpointer=checkpointer, debug=True)
    save_graph_image(graph)
    return graph
