from datetime import datetime
from sqlmodel import Field, Column, SQLModel

from config import config

if config.database.use_local_database:
    from sqlalchemy.dialects.sqlite import JSON

    class Todo(SQLModel, table=True):  # pyright: ignore[reportRedeclaration]
        id: int | None = Field(default=None, primary_key=True)
        title: str = Field(nullable=False, max_length=2 ^ 8)
        is_competed: bool = False
        description: str | None
        completion_date: datetime | None = None
        todo_metadata: dict | None = Field(default={}, sa_column=Column(JSON))
        __tablename__ = "todos"  # pyright: ignore[reportAssignmentType]

else:
    from sqlalchemy.dialects.postgresql import JSONB

    class Todo(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        title: str = Field(nullable=False, max_length=2 ^ 8)
        is_competed: bool = False
        description: str | None
        completion_date: datetime | None = None
        todo_metadata: dict | None = Field(default={}, sa_column=Column(JSONB))
        __tablename__ = "todos"  # pyright: ignore[reportAssignmentType]


class TodoInput(SQLModel):
    title: str
    description: str | None = None
    is_competed: bool = False
    completion_date: datetime | None = None
    todo_metadata: dict | None = None


class TodoUpdate(SQLModel):
    old_id: int
    title: str | None = None
    is_competed: bool | None = None
    description: str | None = None
    completion_date: datetime | None = None
    todo_metadata: dict | None = None


todo_column_names: list[str] = [column.name for column in Todo.__table__.columns]  # pyright: ignore[reportAttributeAccessIssue]
