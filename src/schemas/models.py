import datetime

from pydantic import BaseModel, Field

from src.schemas.constants import TaskStatus


class Task(BaseModel):
    """Модель задачи."""
    id: str = Field(description="ID задачи")
    name: str = Field(description="Название задачи")
    description: str | None = Field(default=None, description="Описание задачи")
    date: datetime.date = Field(description="Дата задачи") 
    date_created: datetime.date = Field(description="Дата создания")
    status: TaskStatus = Field(
        default=TaskStatus.TODO,
        description="Текущий статус задачи",
    )