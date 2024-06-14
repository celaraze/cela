from ..config.database import SessionLocal
from ..database import tables, schemas
from ..utils import common, crypt
from ..models.base import BaseModel
from ..models.user_has_role import UserHasRole
from ..models.role import Role

db = SessionLocal()
table = tables.User
schema = schemas.User


class User:
    @staticmethod
    def select_one(user_id: int):
        return BaseModel.select_one(table, user_id)

    @staticmethod
    def select_one_by_username(username: str):
        conditions = {
            "username": username,
        }
        return BaseModel.select_one_by_columns(table, conditions)

    @staticmethod
    def select_all(skip: int = 0, limit: int = 100):
        return BaseModel.select_all(table, skip, limit)

    @staticmethod
    def create(form_data):
        model_dict = form_data.model_dump()
        hashed_password = crypt.hash_password(model_dict["password"])
        model_dict["hashed_password"] = hashed_password
        model_dict.pop("password")
        model_dict["created_at"] = common.now()
        db_record = table(
            **model_dict,
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record

    @staticmethod
    def update(user_id, form_data: schemas.UpdateForm):
        return BaseModel.update(table, user_id, form_data)

    @staticmethod
    def delete(user_id: int):
        return BaseModel.delete(table, user_id)

    @staticmethod
    def select_roles(user_id: int):
        user_has_roles = UserHasRole.select_all_by_user_id(user_id)
        roles = [Role.select_one(user_has_role.role_id) for user_has_role in user_has_roles]
        return roles

    @staticmethod
    def get_scopes(user_id: int):
        roles = User.select_roles(user_id)
        scopes = []
        for role in roles:
            scopes.extend(role.scopes)
        return scopes
