from enum import StrEnum

class TaskStatus(StrEnum):
    """Статусы задачи."""
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

class ScenarioType(StrEnum):
    TASKS = "TASKS"
    DISCUSSION = "DISCUSSION"