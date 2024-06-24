from fastapi import APIRouter, HTTPException, status, Security
from sqlalchemy import select

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..utils import common
from ..services.todo import get_minutes, check_work, start_work, end_work

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# APIs for Todo.


# Get all todos.
@router.get("/", response_model=list[schemas.Todo])
async def select_todos(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        include_finished: int = 0,
        current_user: schemas.User = Security(get_current_user, scopes=["todo:list"]),
):
    stmt = (
        select(tables.Todo)
        .where(tables.Todo.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    if not include_finished:
        stmt = stmt.where(tables.Todo.is_finished.__eq__(0))
    todos = db.scalars(stmt).all()
    return todos


# Get todo by id.
@router.get("/{todo_id}", response_model=schemas.Todo)
async def select_todo(
        db: databaseSession,
        todo_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["todo:info"]),
):
    stmt = (
        select(tables.Todo)
        .where(tables.Todo.deleted_at.is_(None))
        .where(tables.Todo.id.__eq__(todo_id))
    )
    todo = db.scalars(stmt).one_or_none()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not exists.",
        )
    todo.work_times = get_minutes(db, todo)
    todo.creator = common.get_creator(db, todo.creator_id)
    return todo


# Create todo.
@router.post("/", response_model=schemas.Todo)
async def create_ticket(
        db: databaseSession,
        form_data: schemas.TodoCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["todo:create"]),
):
    form_data.creator_id = current_user.id
    todo = tables.Todo(**form_data.model_dump())
    db.add(todo)
    db.commit()
    return todo


# Update todo.
@router.put("/{todo_id}", response_model=schemas.Todo)
async def update_ticket(
        db: databaseSession,
        todo_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["todo:update"]),
):
    stmt = (
        select(tables.Todo)
        .where(tables.Todo.deleted_at.is_(None))
        .where(tables.Todo.id.__eq__(todo_id))
    )
    todo = db.scalars(stmt).one_or_none()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not exists.",
        )
    for form in form_data:
        setattr(todo, form.key, form.value)
    db.commit()
    return todo


# Delete todo.
@router.delete("/{todo_id}", response_model=schemas.Todo)
async def delete_ticket(
        db: databaseSession,
        todo_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["todo:delete"]),
):
    stmt = (
        select(tables.Todo)
        .where(tables.Todo.deleted_at.is_(None))
        .where(tables.Todo.id.__eq__(todo_id))
    )
    todo = db.scalars(stmt).one_or_none()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not exists.",
        )

    setattr(todo, "deleter_id", current_user.id)
    setattr(todo, "deleted_at", common.now())
    db.commit()
    return todo


# Start work on todo.
@router.post("/{todo_id}/start_work", response_model=schemas.TodoMinute)
async def start_work_on_todo(
        db: databaseSession,
        todo_id: int,
        form_data: schemas.TodoMinuteCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["todo:work"]),
):
    if todo_id != form_data.todo_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Todo id not match.",
        )
    stmt = (
        select(tables.Todo)
        .where(tables.Todo.deleted_at.is_(None))
        .where(tables.Todo.id.__eq__(todo_id))
    )
    todo = db.scalars(stmt).one_or_none()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not exists.",
        )

    minute = check_work(db, todo)
    if minute:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Work on todo already exists.",
        )

    minute = start_work(db, todo, current_user)
    return minute


# End work on todo.
@router.post("/{todo_id}/end_work", response_model=schemas.TodoMinute)
async def end_work_on_ticket(
        db: databaseSession,
        todo_id: int,
        form_data: schemas.TodoMinuteCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["todo:work"]),
):
    if todo_id != form_data.todo_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Todo id not match.",
        )
    stmt = (
        select(tables.Todo)
        .where(tables.Todo.deleted_at.is_(None))
        .where(tables.Todo.id.__eq__(todo_id))
    )
    todo = db.scalars(stmt).one_or_none()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not exists.",
        )

    minute = check_work(db, todo)
    if not minute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work on todo not exists.",
        )
    print(minute)
    minute = end_work(db, todo, current_user)
    return minute
