from langgraph.graph import MessagesState
from langgraph.runtime import Runtime
from src.resources.resources import Resources
from langchain_core.messages import SystemMessage, AIMessage


def call_llm(state: MessagesState, runtime: Runtime[Resources]):

	system_prompt: str = runtime.context.prompts["main_system_prompt"]
	system_msg: SystemMessage = SystemMessage(content=system_prompt)
	ai_msg: AIMessage = runtime.context.llm.invoke([system_msg] + state['messages'])

	return {"messages":  state["messages"] + [ai_msg]}