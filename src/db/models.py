import datetime
import uuid

from sqlalchemy import Date, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.schemas.constants import TaskStatus


class Base(DeclarativeBase):
    pass


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, default=datetime.date.today)
    date_created: Mapped[datetime.date] = mapped_column(Date, nullable=False, default=datetime.date.today)
    status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus), nullable=False, default=TaskStatus.TODO)
