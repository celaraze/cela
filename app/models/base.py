from ..database import schemas


class BaseModel:
    @staticmethod
    def select_one(db, table, model_id: int):
        db_query = db.query(table).filter(table.id.__eq__(model_id))
        return db_query.first()

    @staticmethod
    def select_one_by_columns(db, table, column_values: dict, ):
        db_query = db.query(table)
        for column, value in column_values.items():
            db_query = db_query.filter(getattr(table, column).__eq__(value))
        return db_query.first()

    @staticmethod
    def select_all(db, table, skip: int = 0, limit: int = 100, ):
        db_query = db.query(table)
        return db_query.offset(skip).limit(limit).all()

    @staticmethod
    def select_all_by_columns(db, table, column_values: dict):
        db_query = db.query(table)
        for column, value in column_values.items():
            db_query = db_query.filter(getattr(table, column).__eq__(value))
        return db_query.all()

    @staticmethod
    def select_all_advanced(db, table, conditions: list[schemas.QueryForm]):
        db_query = db.query(table)
        for condition in conditions:
            db_query = db_query.filter(getattr(table, condition.key).__eq__(condition.value))
        return db_query.all()

    @staticmethod
    def create(db, table, form_data):
        model_dict = form_data.model_dump()
        db_record = table(
            **model_dict,
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record

    @staticmethod
    def update(db, table, model_id: int, form_data: schemas.UpdateForm):
        db_record = (
            db.query(table)
            .filter(table.id.__eq__(model_id))
            .first()
        )
        if db_record:
            setattr(db_record, form_data.key, form_data.value)
            db.commit()
            db.refresh(db_record)
        return db_record

    @staticmethod
    def delete(db, table, model_id: int):
        db_record = (
            db.query(table)
            .filter(table.id.__eq__(model_id))
            .first()
        )
        if db_record:
            db.delete(db_record)
            db.commit()
        return db_record

    @staticmethod
    def delete_by_columns(db, table, column_values: dict):
        db_records = BaseModel.select_all_by_columns(db, table, column_values)
        for db_record in db_records:
            if db_record:
                db.delete(db_record)
                db.commit()
        return db_records
