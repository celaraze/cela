from ..config.database import SessionLocal
from ..database import tables, schemas
from ..models.base import BaseModel

db = SessionLocal()
table = tables.Brand
schema = schemas.Brand


class Brand:
    @staticmethod
    def select_one(brand_id: int):
        return BaseModel.select_one(table, brand_id)

    @staticmethod
    def select_one_by_name(name: str):
        conditions = {
            "name": name,
        }
        return BaseModel.select_one_by_columns(table, conditions)

    @staticmethod
    def select_all(skip: int = 0, limit: int = 100):
        return BaseModel.select_all(table, skip, limit)

    @staticmethod
    def create(form_data):
        return BaseModel.create(table, form_data)

    @staticmethod
    def update(brand_id, form_data: schemas.UpdateForm):
        return BaseModel.update(table, brand_id, form_data)

    @staticmethod
    def delete(brand_id: int):
        return BaseModel.delete(table, brand_id)
