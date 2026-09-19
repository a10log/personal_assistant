from dataclasses import dataclass

from pydantic import BaseModel, Field
from langchain_gigachat.chat_models import GigaChat
from src.resources.prompt_provider import SystemPromptProvider


@dataclass
class Resources:
	llm: GigaChat = Field(description="Базовый ЛЛМ провайдер")
	prompts: SystemPromptProvider = Field(description="Подгружает промпты")