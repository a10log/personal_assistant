from sqlalchemy import select, update, delete

from src.db.models import TaskORM
from src.db.session import async_session
from src.schemas.constants import TaskStatus
from src.schemas.models import Task


def _orm_to_task(orm: TaskORM) -> Task:
    """Преобразует ORM-модель в Pydantic-модель."""
    return Task(
        id=orm.id,
        name=orm.name,
        description=orm.description,
        date=orm.date,
        date_created=orm.date_created,
        status=orm.status,
    )


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
            select(TaskORM)
            .where(TaskORM.status == status)
            .order_by(TaskORM.date)
        )
        return [_orm_to_task(orm) for orm in result.scalars()]


async def get_task_by_id(task_id: str) -> Task | None:
    async with async_session() as session:
        result = await session.execute(
            select(TaskORM).where(TaskORM.id == task_id)
        )
        orm = result.scalar_one_or_none()
        return _orm_to_task(orm) if orm else None


async def get_task_by_name(name: str) -> Task | None:
    async with async_session() as session:
        result = await session.execute(
            select(TaskORM).where(TaskORM.name == name)
        )
        orm = result.scalars().first()
        return _orm_to_task(orm) if orm else None


async def update_task_status(task_id: str, new_status: TaskStatus) -> bool:
    async with async_session() as session:
        result = await session.execute(
            update(TaskORM)
            .where(TaskORM.id == task_id)
            .values(status=new_status)
        )
        await session.commit()
        return result.rowcount > 0


async def delete_task(task_id: str) -> bool:
    async with async_session() as session:
        result = await session.execute(
            delete(TaskORM).where(TaskORM.id == task_id)
        )
        await session.commit()
        return result.rowcount > 0