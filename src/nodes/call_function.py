import json
from langgraph.graph import MessagesState
from langgraph.runtime import Runtime
from src.context.context import Context
from langchain_core.messages import ToolMessage, AIMessage
from src.schemas.state import AgentState
from src.tools.tasks import task_tools_dict


async def call_function(state: AgentState, runtime: Runtime[Context]):
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
