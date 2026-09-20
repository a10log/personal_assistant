from langgraph.graph import MessagesState
from pydantic import Field

class AgentState(MessagesState):
	need_function_call: bool = Field(default=False)