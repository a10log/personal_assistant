import yaml
from pathlib import Path

class SystemPromptProvider:

	def __init__(self):
		self._prompts: dict = {}

	def __getitem__(self, name: str):
		return self._prompts[name]

	def _load_yaml(filepath: Path) -> dict:
		with open(filepath, "r", encoding="utf-8") as f:
			return yaml.safe_load(f)
