from langchain_core.messages import AIMessage
from src.schemas.state import AgentState


def route_after_call_llm(state: AgentState) -> str:
    ai_msg: AIMessage = state["messages"][-1]
    if ai_msg.tool_calls:
        return "call_function"
    return "end"