import json

from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langgraph.runtime import Runtime

from src.context.context import Context
from src.scenarios.tasks.tools import task_tools_dict, task_tools_list
from src.schemas.state import AgentState


async def call_llm_with_tools(state: AgentState, runtime: Runtime[Context]):
	system_prompt: str = runtime.context.prompts["main_system_prompt"]
	system_msg: SystemMessage = SystemMessage(content=system_prompt)
	llm_with_tools = runtime.context.llm.bind_tools(task_tools_list)
	ai_msg: AIMessage = await llm_with_tools.ainvoke([system_msg] + state['messages'])
	return {"messages":  state["messages"] + [ai_msg]}


async def call_function(state: AgentState):
	ai_msg: AIMessage = state["messages"][-1]
	tool_msgs: list[ToolMessage] = []
	for tool_call in ai_msg.tool_calls:
		name: str = tool_call["name"]
		args: dict = tool_call["args"]
		id: str = tool_call["id"]

		tool_result = await task_tools_dict[name].ainvoke(args)
		tool_msg = ToolMessage(
			name=name,
			tool_call_id=id,
			content=json.dumps(
				tool_result, 
				ensure_ascii=False,
				  default=str
			),
		)
		tool_msgs.append(tool_msg)
	return {"messages": state["messages"] + tool_msgs}


def check_need_call_function(state: AgentState) -> str:
	if state["messages"][-1].tool_calls:
		return {"need_call_function": True}
	return {"need_call_function": False}


__all__ = ["call_function", "call_llm_with_tools", "check_need_call_function"]