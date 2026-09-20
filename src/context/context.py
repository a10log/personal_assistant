import os
from dataclasses import dataclass

from langchain_gigachat.chat_models import GigaChat
from pydantic import Field

from src.context.prompt_provider import SystemPromptProvider


@dataclass
class Context:
	llm: GigaChat = Field(description="Базовый ЛЛМ провайдер")
	prompts: SystemPromptProvider = Field(description="Подгружает промпты")

def get_context():
	return Context(
		prompts=SystemPromptProvider(),
		llm=GigaChat(
			credentials=os.environ["GIGACHAT_CREDENTIALS"],
			scope=os.environ["GIGACHAT_SCOPE"],
			model=os.environ["GIGACHAT_MODEL"],
			verify_ssl_certs=False,
			timeout=120,
		)
	)