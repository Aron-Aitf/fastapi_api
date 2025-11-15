from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from database import get_session
from models import Todo, TodoUpdate


router = APIRouter(
    prefix="/update",
    tags=["Update"],
)


@router.patch("/update_todo")
def update_todo(
    updates: list[TodoUpdate],
    session: Session = Depends(get_session),
):
    for update in updates:
        if update.title is None:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT, "Title cannot be null"
            )
        if update.is_competed is None:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT, "Is completed cannot be null"
            )

    update_dicts = [data.model_dump(exclude_unset=True) for data in updates]

    for update_dict in update_dicts:
        todo = session.get(Todo, update_dict["old_id"])
        if todo is None:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT, "Invalid todo ids"
            )

        for key, value in update_dict.items():
            if hasattr(todo, key):
                setattr(todo, key, value)

        session.add(todo)
        session.commit()
