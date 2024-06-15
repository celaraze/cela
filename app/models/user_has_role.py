from ..database import tables, schemas
from ..models.base import BaseModel

table = tables.UserHasRole
schema = schemas.UserHasRole


class UserHasRole:
    @staticmethod
    def select_one(db, user_id: int):
        return BaseModel.select_one(db, table, user_id)

    @staticmethod
    def select_one_by_user_id_and_role_id(db, user_id: int, role_id: int):
        conditions = {
            "user_id": user_id,
            "role_id": role_id,
        }
        return BaseModel.select_one_by_columns(db, table, conditions)

    @staticmethod
    def select_all(db, skip: int = 0, limit: int = 100):
        return BaseModel.select_all(db, table, skip, limit)

    @staticmethod
    def select_all_by_user_id(db, user_id: int):
        conditions = {
            "user_id": user_id,
        }
        return BaseModel.select_all_by_columns(db, table, conditions)

    @staticmethod
    def select_all_by_role_id(db, role_id: int):
        conditions = {
            "role_id": role_id,
        }
        return BaseModel.select_all_by_columns(db, table, conditions)

    @staticmethod
    def create(db, form_data):
        return BaseModel.create(db, table, form_data)

    @staticmethod
    def delete(db, user_has_role_id: int):
        return BaseModel.delete(db, table, user_has_role_id)

    @staticmethod
    def delete_by_user_id_and_role_id(db, user_id: int, role_id: int):
        conditions = {
            "user_id": user_id,
            "role_id": role_id,
        }
        return BaseModel.delete_by_columns(db, table, conditions)
