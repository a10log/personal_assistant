import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from src.schemas.http import ChatRequestSchema, ChatResponseSchema
from src.context.context import Context, get_context
from src.graph import get_graph
from src.schemas.state import AgentState

load_dotenv()

app = FastAPI()
graph = get_graph(checkpointer=MemorySaver())
context = get_context()


@app.post("/chat")
async def chat(payload: ChatRequestSchema):
	human_msg: HumanMessage = HumanMessage(content=payload.message)
	thread_id: str = payload.thread_id

	output_state: AgentState = await graph.ainvoke(
		input={"messages": [human_msg]},
		config={"configurable": {"thread_id": thread_id}},
		context=context
	)
	return ChatResponseSchema(
		message=output_state["messages"][-1].content,
		thread_id=thread_id,
	).model_dump()


@app.get("/health")
async def health_check():
	return {"status": "OK"}

if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)