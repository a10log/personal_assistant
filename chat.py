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
    return response.json().get("message", "Пу-пу-пу, что-то пошло не по плану ...")

theme = gr.themes.Default(
    primary_hue="blue",
    secondary_hue="indigo",
    font=["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
)

dark_mode_js = """
() => {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.replace(url);
    }
}
"""

chat = gr.ChatInterface(
    fn=fn,
    title="AI-Ассистент",
    description="Твой помощник для Git, SSH и скриптов",
    examples=[
		"Посмотреть список задач",
        "Создать новую задачу",
    ],
)

if __name__ == "__main__":
    chat.launch(theme=theme, js=dark_mode_js)
