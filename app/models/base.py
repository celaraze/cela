from ..config.database import SessionLocal
from ..database import schemas
from ..utils import common

db = SessionLocal()


class BaseModel:
    @staticmethod
    def select_one(table, user_id: int):
        return (
            db.query(table)
            .filter(table.id.__eq__(user_id))
            .first()
        )

    @staticmethod
    def select_one_by_columns(table, column_values: dict):
        db_query = db.query(table)
        for column, value in column_values.items():
            db_query = db_query.filter(getattr(table, column).__eq__(value))
        return db_query.first()

    @staticmethod
    def select_all(table, skip: int = 0, limit: int = 100):
        return (
            db.query(table)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def select_all_by_columns(table, column_values: dict):
        db_query = db.query(table)
        for column, value in column_values.items():
            db_query = db_query.filter(getattr(table, column).__eq__(value))
        return db_query.all()

    @staticmethod
    def create(table, form_data):
        model_dict = form_data.model_dump()
        model_dict["created_at"] = common.now()
        db_record = table(
            **model_dict,
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record

    @staticmethod
    def update(table, user_id, form_data: schemas.UpdateForm):
        db_record = (
            db.query(table)
            .filter(table.id.__eq__(user_id))
            .first()
        )
        if db_record:
            setattr(db_record, form_data.key, form_data.value)
            db.commit()
            db.refresh(db_record)
        return db_record

    @staticmethod
    def delete(table, user_id: int):
        db_record = (
            db.query(table)
            .filter(table.id.__eq__(user_id))
            .first()
        )
        if db_record:
            db.delete(db_record)
            db.commit()
        return db_record

    @staticmethod
    def delete_by_columns(table, column_values: dict):
        db_records = BaseModel.select_all_by_columns(table, column_values)
        for db_record in db_records:
            if db_record:
                db.delete(db_record)
                db.commit()
        return db_records
