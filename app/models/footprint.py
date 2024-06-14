from ..config.database import SessionLocal
from ..database import tables, schemas
from ..models.base import BaseModel

db = SessionLocal()
table = tables.Footprint
schema = schemas.Footprint


class Footprint:
    @staticmethod
    def select_one(footprint_id: int):
        return BaseModel.select_one(table, footprint_id)

    @staticmethod
    def select_all_by_creator_id(creator_id: int):
        conditions = {
            "creator_id": creator_id,
        }
        return BaseModel.select_all_by_columns(table, conditions)

    @staticmethod
    def select_all(skip: int = 0, limit: int = 100):
        return BaseModel.select_all(table, skip, limit)

    @staticmethod
    def create(form_data):
        return BaseModel.create(table, form_data)
