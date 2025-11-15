from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from models import TodoInput, Todo


router = APIRouter(
    prefix="/add",
    tags=["Add"],
)


@router.post("/add_todo")
def add_todo(
    todo_inputs: list[TodoInput],
    session: Session = Depends(get_session),
):
    todos = [Todo.model_validate(todo_input.model_dump()) for todo_input in todo_inputs]
    session.add_all(todos)
    session.commit()
