import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from src.schemas.http import ChatRequestSchema, ChatResponseSchema
from src.context.context import Context, get_context
from src.graph import get_graph
from src.schemas.state import AgentState
from src.db.session import init_db

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)
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