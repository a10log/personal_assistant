from pydantic import BaseModel

class ChatRequestSchema(BaseModel):
	message: str
	thread_id: str

class ChatResponseSchema(BaseModel):
	message: str
	thread_id: str

	
