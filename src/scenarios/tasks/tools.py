import datetime
from uuid import uuid4

from langchain.tools import tool

from src.db.repo import (
    get_tasks_by_status,
    save_task,
    get_task_by_id,
    get_task_by_name,
    update_task_status,
    delete_task as repo_delete_task,
)
from src.schemas.constants import TaskStatus
from src.schemas.models import Task
from src.utils.tools import get_current_datetime


async def _resolve_task(task_id: str | None, name: str | None) -> Task | None:
    """Находит задачу по id или по имени."""
    if task_id:
        return await get_task_by_id(task_id)
    if name:
        return await get_task_by_name(name)
    return None


@tool
async def create_task(
    name: str,
    description: str | None = None,
    date: str | None = None,
) -> str:
    """
    Создаёт задачу и сохраняет в базу данных.

    Args:
        name: Название задачи.
        description: Описание задачи (необязательно).
        date: Дата в формате YYYY-MM-DD. Если не указана — сегодняшняя.
    """
    if date is None:
        parsed_date = datetime.date.today()
    else:
        parsed_date = datetime.date.fromisoformat(date)

    task = Task(
        id=str(uuid4()),
        name=name,
        description=description,
        date=parsed_date,
        date_created=datetime.date.today(),
        status=TaskStatus.TODO,
    )
    await save_task(task)
    return f"Задача «{name}» создана на {parsed_date.isoformat()}"


@tool
async def get_todo_task_list() -> str:
    """Возвращает список невыполненных задач."""
    tasks = await get_tasks_by_status(TaskStatus.TODO)
    if not tasks:
        return "Список задач пуст."
    lines = []
    for t in tasks:
        desc = f" — {t.description}" if t.description else ""
        lines.append(f"• {t.name} (до {t.date.isoformat()}){desc}")
    return "\n".join(lines)


@tool
async def complete_task(
    task_id: str | None = None,
    name: str | None = None,
) -> str:
    """
    Отмечает задачу как выполненную (статус DONE).

    Args:
        task_id: ID задачи (если известен).
        name: Название задачи (используется, если ID не указан).
    """
    task = await _resolve_task(task_id, name)
    if task is None:
        return "Задача не найдена."
    if task.status == TaskStatus.DONE:
        return f"Задача «{task.name}» уже выполнена."
    await update_task_status(task.id, TaskStatus.DONE)
    return f"Задача «{task.name}» отмечена как выполненная."


@tool
async def cancel_task(
    task_id: str | None = None,
    name: str | None = None,
) -> str:
    """
    Отменяет задачу (статус CANCELLED).

    Args:
        task_id: ID задачи (если известен).
        name: Название задачи (используется, если ID не указан).
    """
    task = await _resolve_task(task_id, name)
    if task is None:
        return "Задача не найдена."
    if task.status == TaskStatus.CANCELLED:
        return f"Задача «{task.name}» уже отменена."
    await update_task_status(task.id, TaskStatus.CANCELLED)
    return f"Задача «{task.name}» отменена."


@tool
async def delete_task(
    task_id: str | None = None,
    name: str | None = None,
) -> str:
    """
    Полностью удаляет задачу из базы данных.

    Args:
        task_id: ID задачи (если известен).
        name: Название задачи (используется, если ID не указан).
    """
    task = await _resolve_task(task_id, name)
    if task is None:
        return "Задача не найдена."
    await repo_delete_task(task.id)
    return f"Задача «{task.name}» удалена."


task_tools_list: list = [
    create_task,
    get_todo_task_list,
    complete_task,
    cancel_task,
    delete_task,
    get_current_datetime,
]
task_tools_dict: dict = {tool.name: tool for tool in task_tools_list}


__all__ = ["task_tools_dict", "task_tools_list"]