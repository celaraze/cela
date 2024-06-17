from ..database import tables, schemas
from ..models.base import BaseModel

table = tables.Device
schema = schemas.Device


class Device:
    @staticmethod
    def select_one(db, device_id: int):
        return BaseModel.select_one(db, table, device_id)

    @staticmethod
    def select_one_by_asset_number(db, asset_number: str):
        conditions = {
            "asset_number": asset_number,
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
    def update(db, device_id, form_data: schemas.UpdateForm):
        return BaseModel.update(db, table, device_id, form_data)

    @staticmethod
    def delete(db, device_id: int):
        return BaseModel.delete(db, table, device_id)
