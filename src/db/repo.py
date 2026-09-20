
from sqlalchemy import select

from src.db.models import TaskORM
from src.db.session import async_session
from src.schemas.constants import TaskStatus
from src.schemas.models import Task


async def save_task(task: Task) -> Task:
    async with async_session() as session:
        orm = TaskORM(
            id=task.id,
            name=task.name,
            description=task.description,
            date=task.date,
            date_created=task.date_created,
            status=task.status,
        )
        session.add(orm)
        await session.commit()
        return task

async def get_tasks_by_status(status: TaskStatus) -> list[Task]:
    async with async_session() as session:
        result = await session.execute(
            select(TaskORM).where(TaskORM.status == status).order_by(TaskORM.date)
        )
        return [
            Task(
                id=orm.id,
                name=orm.name,
                description=orm.description,
                date=orm.date,
                date_created=orm.date_created,
                status=orm.status,
            )
            for orm in result.scalars()
        ]