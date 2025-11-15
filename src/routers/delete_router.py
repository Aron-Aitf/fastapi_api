from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session, delete, select
from database import get_session
from models import Todo


router = APIRouter(
    prefix="/delete",
    tags=["Delete"],
)


@router.delete("/delete_todo")
def delete_todo(
    todo_ids: list[int] = Query(),
    session: Session = Depends(get_session),
):
    if not session.exec(select(Todo).where(Todo.id.in_(todo_ids))).all() == todo_ids:  # pyright: ignore[reportAttributeAccessIssue, reportOptionalMemberAccess]
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Invalid Ids")
    statement = delete(Todo).where(Todo.id.in_(todo_ids))  # pyright: ignore[reportAttributeAccessIssue, reportOptionalMemberAccess]
    session.exec(statement)
    session.commit()
