from ..database import tables, schemas
from ..utils import crypt
from ..models.base import BaseModel
from ..models.user_has_role import UserHasRole
from ..models.role import Role

table = tables.User
schema = schemas.User


class User:
    @staticmethod
    def select_one(db, user_id: int):
        return BaseModel.select_one(db, table, user_id)

    @staticmethod
    def select_one_by_username(db, username: str):
        conditions = {
            "username": username,
        }
        return BaseModel.select_one_by_columns(db, table, conditions)

    @staticmethod
    def select_one_by_email(db, email: str):
        conditions = {
            "email": email,
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
        model_dict = form_data.model_dump()
        hashed_password = crypt.hash_password(model_dict["password"])
        model_dict["hashed_password"] = hashed_password
        model_dict.pop("password")
        db_record = table(
            **model_dict,
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record

    @staticmethod
    def update(db, user_id, form_data: schemas.UpdateForm):
        return BaseModel.update(db, table, user_id, form_data)

    @staticmethod
    def delete(db, user_id: int):
        return BaseModel.delete(db, table, user_id)

    @staticmethod
    def select_roles(db, user_id: int):
        user_has_roles = UserHasRole.select_all_by_user_id(db, user_id)
        roles = [Role.select_one(db, user_has_role.role_id) for user_has_role in user_has_roles]
        return roles

    @staticmethod
    def get_scopes(db, user_id: int):
        roles = User.select_roles(db, user_id)
        scopes = []
        for role in roles:
            scopes.extend(role.scopes)
        return scopes
