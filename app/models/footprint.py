from ..database import tables, schemas
from ..models.base import BaseModel

table = tables.Footprint
schema = schemas.Footprint


class Footprint:
    @staticmethod
    def select_one(db, footprint_id: int):
        return BaseModel.select_one(db, table, footprint_id)

    @staticmethod
    def select_all_by_creator_id(db, creator_id: int):
        conditions = {
            "creator_id": creator_id,
        }
        return BaseModel.select_all_by_columns(db, table, conditions)

    @staticmethod
    def select_all(db, skip: int = 0, limit: int = 100):
        return BaseModel.select_all(db, table, skip, limit)

    @staticmethod
    def create(db, form_data):
        return BaseModel.create(db, table, form_data)
