from ..config.database import SessionLocal
from ..database import tables, schemas
from ..models.base import BaseModel

db = SessionLocal()
table = tables.DeviceCategory
schema = schemas.DeviceCategory


class DeviceCategory:
    @staticmethod
    def select_one(device_category_id: int):
        return BaseModel.select_one(table, device_category_id)

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
    def update(device_category_id, form_data: schemas.UpdateForm):
        return BaseModel.update(table, device_category_id, form_data)

    @staticmethod
    def delete(device_category_id: int):
        return BaseModel.delete(table, device_category_id)
