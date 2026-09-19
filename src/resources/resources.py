from pydantic import BaseModel, Field
from langchain_gigachat.chat_models import GigaChat
from src.resources.prompt_provider import SystemPromptProvider

class Resources(BaseModel):
	llm: GigaChat = Field(description="Базовый ЛЛМ провайдер")
	prompt_provider: SystemPromptProvider = Field(description="Подгружает промпты")