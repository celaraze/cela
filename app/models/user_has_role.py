from ..config.database import SessionLocal
from ..database import tables, schemas
from ..models.base import BaseModel

db = SessionLocal()
table = tables.UserHasRole
schema = schemas.UserHasRole


class UserHasRole:
    @staticmethod
    def select_one(user_id: int):
        return BaseModel.select_one(table, user_id)

    @staticmethod
    def select_one_by_user_id_and_role_id(user_id: int, role_id: int):
        conditions = {
            "user_id": user_id,
            "role_id": role_id,
        }
        return BaseModel.select_one_by_columns(table, conditions)

    @staticmethod
    def select_all(skip: int = 0, limit: int = 100):
        return BaseModel.select_all(table, skip, limit)

    @staticmethod
    def select_all_by_user_id(user_id: int):
        conditions = {
            "user_id": user_id,
        }
        return BaseModel.select_all_by_columns(table, conditions)

    @staticmethod
    def select_all_by_role_id(role_id: int):
        conditions = {
            "role_id": role_id,
        }
        return BaseModel.select_all_by_columns(table, conditions)

    @staticmethod
    def create(form_data):
        return BaseModel.create(table, form_data)

    @staticmethod
    def delete(user_has_role_id: int):
        return BaseModel.delete(table, user_has_role_id)

    @staticmethod
    def delete_by_user_id_and_role_id(user_id: int, role_id: int):
        conditions = {
            "user_id": user_id,
            "role_id": role_id,
        }
        return BaseModel.delete_by_columns(table, conditions)
