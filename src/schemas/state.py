from langgraph.graph import MessagesState
from pydantic import Field

from src.schemas.constants import ScenarioType


class AgentState(MessagesState):
	need_call_function: bool = Field(default=False)
	scenario_type: ScenarioType = Field(
		default=ScenarioType.DISCUSSION,  
		description="Тип текущего сценария",
	)
