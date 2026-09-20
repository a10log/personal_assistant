import yaml
from pathlib import Path

PROMPTS_DIR = "prompts"

class SystemPromptProvider:

	def __init__(self):
		self._prompts: dict = {}
		self._load_prompts()

	def __getitem__(self, name: str):
		return self._prompts[name]

	@staticmethod
	def _load_yaml(filepath: Path) -> dict:
		with open(filepath, "r", encoding="utf-8") as f:
			return yaml.safe_load(f)
		
	def _load_prompts(self):
		for filepath in Path(PROMPTS_DIR).iterdir():
			data: dict = self._load_yaml(filepath)
			name: str = filepath.name.replace(".yaml","")
			self._prompts[name] = data["prompt"]


