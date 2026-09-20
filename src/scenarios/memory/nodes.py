from src.schemas.state import AgentState

def trim_history(state: AgentState, target_messages: int = 10) -> dict:
    return {"messages":  state["messages"][-target_messages:]}

