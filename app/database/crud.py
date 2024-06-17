from typing import Any

from ..database import schemas
from ..utils import common


def select(
        db,
        table,
        condition: schemas.QueryForm,
        trashed_column: str = "deleted_at",
        with_trashed: bool = False,
):
    db_query = db.query(table)
    if condition.operator == "==":
        if condition.value is None:
            db_query = db_query.filter(getattr(table, condition.key).is_(None))
        else:
            db_query = db_query.filter(getattr(table, condition.key).__eq__(condition.value))
    elif condition.operator == "!=":
        if condition.value is None:
            db_query = db_query.filter(getattr(table, condition.key).isnot(None))
        else:
            db_query = db_query.filter(getattr(table, condition.key).__ne__(condition.value))
    elif condition.operator == "like":
        db_query = db_query.filter(getattr(table, condition.key).like(f"%{condition.value}%"))
    else:
        pass
    if not with_trashed:
        db_query = db_query.filter(getattr(table, trashed_column).is_(None))
    return db_query.all()


def selects(
        db,
        table,
        conditions: list[schemas.QueryForm],
        trashed_column: str = "deleted_at",
        with_trashed: bool = False,
):
    db_query = db.query(table)
    for condition in conditions:
        if condition.operator == "==":
            if condition.value is None:
                db_query = db_query.filter(getattr(table, condition.key).is_(None))
            else:
                db_query = db_query.filter(getattr(table, condition.key).__eq__(condition.value))
        elif condition.operator == "!=":
            if condition.value is None:
                db_query = db_query.filter(getattr(table, condition.key).isnot(None))
            else:
                db_query = db_query.filter(getattr(table, condition.key).__ne__(condition.value))
        elif condition.operator == "like":
            db_query = db_query.filter(getattr(table, condition.key).like(f"%{condition.value}%"))
        else:
            continue
    if not with_trashed:
        db_query = db_query.filter(getattr(table, trashed_column).is_(None))
    return db_query.all()


def select_id(
        db,
        table,
        primary_id,
        with_trashed=False
):
    condition = schemas.QueryForm(key="id", operator="==", value=primary_id)
    records = select(db, table, condition, with_trashed=with_trashed)
    if records:
        return records[0]
    return None


def select_username(db, table, username):
    condition = schemas.QueryForm(key="username", operator="==", value=username)
    records = select(db, table, condition)
    if records:
        return records[0]
    return None


def select_name(db, table, name):
    condition = schemas.QueryForm(key="name", operator="==", value=name)
    records = select(db, table, condition)
    if records:
        return records[0]
    return None


def select_asset_number(db, table, asset_number):
    condition = schemas.QueryForm(key="asset_number", operator="==", value=asset_number)
    records = select(db, table, condition)
    if records:
        return records[0]
    return None


def select_all_with_trashed(db, table, primary_id) -> list[Any]:
    db_query = (
        db.query(table)
        .filter(table.id.__eq__(primary_id))
        .filter(getattr(table, deleted_at_column).isnot(None))
    )
    return db_query.all()


def select_all(db, table, skip: int = 0, limit: int = 100, deleted_at_column: str = "deleted_at") -> list[Any]:
    db_query = db.query(table)
    db_query = db_query.filter(getattr(table, deleted_at_column).is_(None))
    return db_query.offset(skip).limit(limit).all()


def select_all_with_trashed(
        db,
        table,
        skip: int = 0,
        limit: int = 100,
        deleted_at_column: str = "deleted_at"
) -> list[Any]:
    db_query = db.query(table)
    db_query = db_query.filter(getattr(table, deleted_at_column).isnot(None))
    return db_query.offset(skip).limit(limit).all()


def create(db, table, form_data) -> list[Any]:
    model_dict = form_data.model_dump()
    db_record = table(
        **model_dict,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return [db_record]


def update(db, table, primary_id, form_data: schemas.UpdateForm) -> list[Any]:
    db_records = select(db, table, primary_id)
    if db_records:
        setattr(db_records[0], form_data.key, form_data.value)
    db.commit()
    db.refresh(db_records[0])
    return db_records


def delete(db, table, primary_id, deleted_at_column: str = "deleted_at") -> list[Any]:
    db_records = select(db, table, primary_id)
    if db_records:
        setattr(db_records[0], deleted_at_column, common.now())
        db.commit()
        db.refresh(db_records[0])
    return db_records


def restore(db, table, primary_id) -> list[Any]:
    update_form = schemas.UpdateForm(key="deleted_at", value=None)
    return update(db, table, primary_id, update_form)


def force_delete(db, table, primary_id) -> list[Any]:
    db_records = select_with_trashed(db, table, primary_id)
    if db_records:
        db.delete(db_records[0])
        db.refresh(db_records[0])
    return db_records
