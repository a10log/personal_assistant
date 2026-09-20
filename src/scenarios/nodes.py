from langgraph.runtime import Runtime
from langchain_core.messages import SystemMessage
from src.context.context import Context
from src.schemas.state import AgentState
from src.schemas.output import ClassifyScenarioOutputSchema

async def classify_scenario(state: AgentState, runtime: Runtime[Context]):
	system_prompt: str = runtime.context.prompts["main_system_prompt"]
	instructions_prompt: str = runtime.context.prompts["classify_scenario"]
	system_msg: SystemMessage = SystemMessage(
		content=f"{system_prompt}\n\n{instructions_prompt}"
	)
	llm = runtime.context.llm.with_structured_output(ClassifyScenarioOutputSchema)
	answer: ClassifyScenarioOutputSchema = await llm.ainvoke([system_msg] + state["messages"])

	return {"scenario_type": answer.scenario_type}