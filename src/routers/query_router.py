from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Annotated, Any, Literal
from sqlmodel import SQLModel, Session, asc, select, desc
from database import get_session
from models import Todo, todo_column_names


router = APIRouter(
    prefix="/query",
    tags=["Query"],
)


def table_dicts(data: tuple, column_names: list[str]) -> list[dict[str, Any]]:
    list_of_dicts = []
    for row in data:
        row_dict = dict(zip(column_names, row))
        list_of_dicts.append(row_dict)
    return list_of_dicts


def sort_from_dict(query, sort_dict: dict, model_class: type[SQLModel]):
    order_by_expressions = []
    for col_name, sort_direction in sort_dict.items():
        column_attr = getattr(model_class, col_name, None)
        if column_attr is not None:
            if sort_direction.lower() == "descending":
                order_by_expressions.append(desc(column_attr))  # pyright: ignore[reportArgumentType]
            elif sort_direction.lower() == "ascending" or sort_direction.lower() == "":
                order_by_expressions.append(asc(column_attr))  # pyright: ignore[reportArgumentType]
    if order_by_expressions:
        query = query.order_by(*order_by_expressions)
    return query


@router.post("/get_todos")
def get_todos(
    offset: int = Query(default=0, gt=-1),
    limit: int = Query(default=2 ^ 8, le=(2 ^ 8) * 10, ge=0),
    fields: Annotated[list[str], Query()] = todo_column_names,
    sort_dict: dict[str, Literal["ascending"] | Literal["descending"]] = {},
    session: Session = Depends(get_session),
) -> list[dict[str, Any]]:
    if not set(fields).issubset(todo_column_names):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid Fields"
        )
    if not set(sort_dict.keys()).issubset(todo_column_names):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid Fields in sort dict"
        )

    selected_columns = [getattr(Todo, field_name) for field_name in fields]
    statement = sort_from_dict(
        select(*selected_columns).offset(offset).limit(limit), sort_dict, Todo
    )
    return table_dicts(session.exec(statement).all(), fields)
