
from langgraph.runtime import Runtime
from src.context.context import Context
from langchain_core.messages import SystemMessage, AIMessage
from src.schemas.state import AgentState
from src.tools.tasks import task_tools_list


def call_llm(state: AgentState, runtime: Runtime[Context]):
	system_prompt: str = runtime.context.prompts["main_system_prompt"]
	system_msg: SystemMessage = SystemMessage(content=system_prompt)
	ai_msg: AIMessage = runtime.context.llm.invoke([system_msg] + state['messages'])

	return {"messages":  state["messages"] + [ai_msg]}


def call_llm_with_tools(state: AgentState, runtime: Runtime[Context]):
	system_prompt: str = runtime.context.prompts["main_system_prompt"]
	system_msg: SystemMessage = SystemMessage(content=system_prompt)
	llm_with_tools = runtime.context.llm.bind_tools(task_tools_list)
	ai_msg: AIMessage = llm_with_tools.invoke([system_msg] + state['messages'])
	
	return {"messages":  state["messages"] + [ai_msg]}