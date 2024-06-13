from sqlalchemy.orm import Session, joinedload

from ..utils import crypt
from ..database import tables, schemas
from ..utils import common


class User:
    @staticmethod
    def select_one(db: Session, user_id: int):
        return (
            db.query(tables.User)
            .filter(tables.User.id.__eq__(user_id))
            .first()
        )

    @staticmethod
    def select_one_by_username(db: Session, username: str):
        return (
            db.query(tables.User)
            .options(joinedload(tables.User.roles))
            .filter(tables.User.username.__eq__(username))
            .first()
        )

    @staticmethod
    def select_all(db: Session, skip: int = 0, limit: int = 100):
        return (
            db.query(tables.User)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, user: schemas.UserForm) -> tables.User:
        hashed_password = crypt.hash_password(user.password)
        user_dict = user.model_dump()
        user_dict.pop("password")
        user_dict["hashed_password"] = hashed_password
        user_dict["creator_id"] = user.creator_id
        user_dict["created_at"] = common.now()
        db_user = tables.User(
            **user_dict,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update(db: Session, user: schemas.User, form_data: schemas.UpdateForm):
        db_user = (
            db.query(tables.User)
            .filter(tables.User.id.__eq__(user.id))
            .first()
        )
        if db_user:
            setattr(db_user, form_data.key, form_data.value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete(db: Session, user_id: int):
        db_user = (
            db.query(tables.User)
            .filter(tables.User.id.__eq__(user_id))
            .first()
        )
        if db_user:
            db_user.deleted_at = common.now()
            db.commit()
            db.refresh(db_user)
        return db_user
