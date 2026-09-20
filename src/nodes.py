from langchain_core.messages import SystemMessage
from langgraph.runtime import Runtime

from src.context.context import AgentContext
from src.schemas.output import ClassifyScenarioOutputSchema
from src.schemas.state import AgentState


async def classify_scenario(state: AgentState, runtime: Runtime[AgentContext]) -> dict:
	system_prompt: str = runtime.context.prompts["main_system_prompt"]
	instructions_prompt: str = runtime.context.prompts["classify_scenario"]
	system_msg: SystemMessage = SystemMessage(
		content=f"{system_prompt}\n\n{instructions_prompt}"
	)
	llm = runtime.context.llm.with_structured_output(ClassifyScenarioOutputSchema)
	answer: ClassifyScenarioOutputSchema = await llm.ainvoke([system_msg] + state["messages"])

	return {"scenario_type": answer.scenario_type}
