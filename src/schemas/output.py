from pydantic import BaseModel, Field

from src.schemas.constants import ScenarioType


class ClassifyScenarioOutputSchema(BaseModel):
	"""Схема для ноды classify_scenario"""
	scenario_type: ScenarioType = Field(description="Тип сценария")
