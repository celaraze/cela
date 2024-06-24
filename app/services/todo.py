from sqlalchemy import select

from app.database import tables, schemas


def get_minutes(db, todo):
    stmt = (
        select(tables.TodoMinute)
        .where(tables.TodoMinute.deleted_at.is_(None))
        .where(tables.TodoMinute.todo_id.__eq__(todo.id))
    )
    minutes = db.scalars(stmt).all()
    return minutes


def check_work(db, todo):
    stmt = (
        select(tables.TodoMinute)
        .where(tables.TodoMinute.deleted_at.is_(None))
        .where(tables.TodoMinute.is_finished.__eq__(0))
        .where(tables.TodoMinute.todo_id.__eq__(todo.id))
        .where(tables.TodoMinute.flag.__eq__(0))
    )
    minute = db.scalars(stmt).one_or_none()
    return minute


def start_work(db, todo, user):
    form_data = schemas.TodoMinuteCreateForm(
        todo_id=todo.id,
        flag=0,
        creator_id=user.id,
    )
    minute = tables.TodoMinute(**form_data.model_dump())
    db.add(minute)
    db.commit()
    return minute


def end_work(db, todo, user):
    form_data = schemas.TodoMinuteCreateForm(
        todo_id=todo.id,
        flag=1,
        creator_id=user.id,
    )
    minute = tables.TodoMinute(**form_data.model_dump())
    db.add(minute)
    db.commit()

    stmt = (
        select(tables.TodoMinute)
        .where(tables.TodoMinute.deleted_at.is_(None))
        .where(tables.TodoMinute.todo_id.__eq__(todo.id))
        .where(tables.TodoMinute.flag.__eq__(0))
        .where(tables.TodoMinute.is_finished.__eq__(0))
    )
    minutes = db.scalars(stmt).all()
    for minute in minutes:
        minute.is_finished = 1
        db.commit()
    return minute
