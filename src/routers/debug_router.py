from fastapi import APIRouter, Depends, Query
from faker import Faker
from json import load

from sqlmodel import SQLModel, Session

from database import get_session
from models import Todo

NUM_FAKE_TODO_TITLES = 2 ^ 8

fake = Faker()

router = APIRouter(
    prefix="/debug",
    tags=["Debug"],
)


@router.get("/populate_fake_data")
def populate_fake_data(
    number: int = Query(
        default=NUM_FAKE_TODO_TITLES * 2, gt=0, lt=NUM_FAKE_TODO_TITLES * 200
    ),
    session: Session = Depends(get_session),
):
    with open("./data/todo_list.json", "r") as file:
        todos = load(file)[:number]

    todos = [Todo.model_validate(todo) for todo in todos]
    session.add_all(todos)
    session.commit()
    pass


@router.delete("/delete_all")
def clear_database(
    session: Session = Depends(get_session),
):
    for table in reversed(SQLModel.metadata.sorted_tables):
        session.exec(table.delete())
    session.commit()
# [0-9][0-9][0-9]