from ..config.database import SessionLocal
from ..database import tables, schemas
from ..models.base import BaseModel

table = tables.Brand
schema = schemas.Brand


class Brand:
    @staticmethod
    def select_one(db, brand_id: int):
        return BaseModel.select_one(db, table, brand_id)

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
    def create(db, form_data):
        return BaseModel.create(db, table, form_data)

    @staticmethod
    def update(db, brand_id, form_data: schemas.UpdateForm):
        return BaseModel.update(db, table, brand_id, form_data)

    @staticmethod
    def delete(db, brand_id: int):
        return BaseModel.delete(db, table, brand_id)
