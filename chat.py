import gradio as gr
import requests
from urllib.parse import urljoin
from src.schemas.http import ChatRequestSchema


BASE_AGENT_URL = "http://127.0.0.1:8000"
THREAD_ID = "my-thread-id"

def send_response_to_agent(message):
	return requests.post(
		url=urljoin(BASE_AGENT_URL, "chat"), 
		json=ChatRequestSchema(
			message=message,
			thread_id=THREAD_ID
		).model_dump()
	)

def fn(message, history):
	response = send_response_to_agent(message)
	return response.json().get("message")

chat = gr.ChatInterface(
    fn=fn,
    title="Простой чат",
    description="Базовый чат на Gradio"
)

if __name__ == "__main__":
	chat.launch()