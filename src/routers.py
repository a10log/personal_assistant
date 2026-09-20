from langchain_core.runnables import RunnableConfig
from src.schemas.state import AgentState

async def route_mode(_, config: RunnableConfig) -> str:
    mode = config.get("configurable", {}).get("mode", "chat")
    if mode == "memory":
        return "manage_memory"
    return "chat"

# TODO
async def route_after_classify_scenario(state: AgentState):
    pass