from ..database import tables, schemas
from ..models.base import BaseModel

table = tables.Role
schema = schemas.Role


class Role:
    @staticmethod
    def select_one(db, user_id: int):
        return BaseModel.select_one(db, table, user_id)

    @staticmethod
    def select_one_by_name(db, name: str):
        conditions = {
            "name": name,
        }
        return BaseModel.select_one_by_columns(db, table, conditions)

    @staticmethod
    def select_all(db, skip: int = 0, limit: int = 100):
        return BaseModel.select_all(db, table, skip, limit)

    @staticmethod
    def select_all_advanced(db, conditions: list[schemas.QueryForm]):
        return BaseModel.select_all_advanced(db, table, conditions)

    @staticmethod
    def create(db, form_data):
        return BaseModel.create(db, table, form_data)

    @staticmethod
    def update(db, user_id: int, form_data: schemas.UpdateForm):
        return BaseModel.update(db, table, user_id, form_data)

    @staticmethod
    def delete(db, user_id: int):
        return BaseModel.delete(db, table, user_id)
