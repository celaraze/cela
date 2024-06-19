from typing import Any

from sqlalchemy.orm import make_transient

from ..database import schemas
from ..utils import common, crypt

PRIMARY_ID = "id"
SOFT_DELETE = "deleted_at"


def selects(
        db,
        table,
        conditions: list[schemas.QueryForm],
        with_trashed: bool = False,
        skip: int = None,
        limit: int = None,
):
    db_query = db.query(table)
    for condition in conditions:
        if condition.key == SOFT_DELETE:
            continue
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
        db_query = db_query.filter(getattr(table, SOFT_DELETE).is_(None))
    if skip:
        db_query = db_query.offset(skip)
    if limit:
        db_query = db_query.limit(limit)
    return db_query.all()


def select(
        db,
        table,
        key,
        operator,
        value,
        with_trashed: bool = False,
        skip: int = None,
        limit: int = None,
):
    db_query = db.query(table)
    if operator == "!=":
        if value is None:
            db_query = db_query.filter(getattr(table, key).isnot(None))
        else:
            db_query = db_query.filter(getattr(table, key).__ne__(value))
    elif operator == "like":
        db_query = db_query.filter(getattr(table, key).like(f"%{value}%"))
    else:
        if value is None:
            db_query = db_query.filter(getattr(table, key).is_(None))
        else:
            db_query = db_query.filter(getattr(table, key).__eq__(value))
    if not with_trashed:
        db_query = db_query.filter(getattr(table, SOFT_DELETE).is_(None))
    if skip:
        db_query = db_query.offset(skip)
    if limit:
        db_query = db_query.limit(limit)
    return db_query.all()


def select_id(
        db,
        table,
        primary_id,
        with_trashed: bool = False,
):
    results = select(db, table, PRIMARY_ID, "==", primary_id, with_trashed=with_trashed)
    return results[0] if results else None


def select_username(
        db,
        table,
        username,
        with_trashed: bool = False,
):
    results = select(db, table, "username", "==", username, with_trashed=with_trashed)
    return results[0] if results else None


def select_email(
        db,
        table,
        email,
        with_trashed: bool = False,
):
    results = select(db, table, "email", "==", email, with_trashed=with_trashed)
    return results[0] if results else None


def select_name(
        db,
        table,
        name,
        with_trashed: bool = False,
):
    results = select(db, table, "name", "==", name, with_trashed=with_trashed)
    return results[0] if results else None


def select_asset_number(
        db,
        table,
        asset_number,
        with_trashed: bool = False,
):
    results = select(db, table, "asset_number", "==", asset_number, with_trashed=with_trashed)
    return results[0] if results else None


def select_all(
        db,
        table,
        conditions: list[schemas.QueryForm] = None,
        skip: int = None,
        limit: int = None,
) -> list[Any]:
    if conditions is None:
        conditions = []
    results = selects(db, table, conditions, skip=skip, limit=limit)
    return results


def select_all_with_trashed(
        db,
        table,
        conditions: list[schemas.QueryForm] = None,
        skip: int = None,
        limit: int = None,
) -> list[Any]:
    if conditions is None:
        conditions = []
    results = selects(db, table, conditions, with_trashed=True, skip=skip, limit=limit)
    return results


def create(db, table, form_data):
    model_dict = form_data.model_dump()
    db_record = table(**model_dict)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def create_user(db, table, form_data):
    model_dict = form_data.model_dump()
    model_dict['hashed_password'] = crypt.hash_password(model_dict['password'])
    model_dict.pop('password')
    db_record = table(
        **model_dict,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update(
        db,
        table,
        primary_id,
        form_data: list[schemas.UpdateForm],
        with_trashed: bool = False,
):
    db_record = select_id(db, table, primary_id, with_trashed=with_trashed)
    if db_record:
        for update_form in form_data:
            setattr(db_record, update_form.key, update_form.value)
    db.commit()
    db.refresh(db_record)
    return db_record


def delete(
        db,
        table,
        primary_id,
):
    db_record = select_id(db, table, primary_id)
    if db_record:
        setattr(db_record, SOFT_DELETE, common.now())
        db.commit()
        db.refresh(db_record)
    return db_record


def delete_conditions(
        db,
        table,
        conditions: list[schemas.QueryForm],
):
    db_records = select_all(db, table, conditions)
    for db_record in db_records:
        setattr(db_record, SOFT_DELETE, common.now())
    db.commit()
    return db_records


def restore(
        db,
        table,
        primary_id,
):
    update_form = [
        schemas.UpdateForm(key=SOFT_DELETE, value=None),
    ]
    return update(db, table, primary_id, update_form, with_trashed=True)


def force_delete(
        db,
        table,
        primary_id,
):
    db_record = select_id(db, table, primary_id, with_trashed=True)
    if db_record:
        db.delete(db_record)
    return db_record


def force_delete_conditions(
        db,
        table,
        conditions: list[schemas.QueryForm],
):
    db_records = select_all_with_trashed(db, table, conditions)
    for db_record in db_records:
        db.delete(db_record)
    return db_records


def copy(
        db,
        table,
        db_record
):
    record_dict = db_record.__dict__.copy()
    record_dict.pop('_sa_instance_state', None)
    new_db_record = table(**record_dict)
    make_transient(new_db_record)
    new_db_record.id = None
    db.add(new_db_record)
    db.commit()
    db.refresh(new_db_record)
    return new_db_record


def select_creator(
        db,
        table,
        creator_id,
):
    creator = select_id(db, table, creator_id)
    if not creator:
        return None
    return creator
