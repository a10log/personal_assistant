import datetime
from uuid import uuid4
from langchain.tools import tool
from src.schemas.models import Task
from src.schemas.constants import TaskStatus
from src.tools.utils import get_current_datetime
from src.db.repo import save_task, get_tasks_by_status

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


task_tools_list : list = [create_task, get_todo_task_list, get_current_datetime]
task_tools_dict: dict = {tool.name: tool for tool in task_tools_list}