from sqlalchemy.orm import Session

from ..database import tables, schemas


class UserHasRole:
    @staticmethod
    def select_one(db: Session, user_has_role_id: int):
        return (
            db.query(tables.UserHasRole)
            .filter(tables.UserHasRole.id.__eq__(user_has_role_id))
            .first()
        )

    @staticmethod
    def select_all_by_user_id(db: Session, user_id: int):
        return (
            db.query(tables.UserHasRole)
            .filter(tables.UserHasRole.user_id.__eq__(user_id))
            .all()
        )

    @staticmethod
    def select_all_by_role_id(db: Session, role_id: int):
        return (
            db.query(tables.UserHasRole)
            .filter(tables.UserHasRole.role_id.__eq__(role_id))
            .all()
        )

    @staticmethod
    def select_one_by_user_id_and_role_id(db: Session, user_id: int, role_id: int):
        return (
            db.query(tables.UserHasRole)
            .filter(tables.UserHasRole.user_id.__eq__(user_id))
            .filter(tables.UserHasRole.role_id.__eq__(role_id))
            .first()
        )

    @staticmethod
    def select_all(db: Session, skip: int = 0, limit: int = 100):
        return (
            db.query(tables.UserHasRole)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, user_has_role: schemas.UserHasRoleForm):
        user_has_role_dict = user_has_role.model_dump()
        db_user_has_role = tables.UserHasRole(
            **user_has_role_dict,
        )
        db.add(db_user_has_role)
        db.commit()
        db.refresh(db_user_has_role)
        return db_user_has_role

    @staticmethod
    def delete(db: Session, user_has_role_id: int):
        db_user_has_role = (
            db.query(tables.UserHasRole)
            .filter(tables.UserHasRole.id.__eq__(user_has_role_id))
            .first()
        )
        if db_user_has_role:
            db.delete(db_user_has_role)
            db.commit()
        return db_user_has_role

    @staticmethod
    def delete_by_user_id_and_role_id(db: Session, user_id: int, role_id: int):
        db_user_has_role = (
            db.query(tables.UserHasRole)
            .filter(tables.UserHasRole.user_id.__eq__(user_id))
            .filter(tables.UserHasRole.role_id.__eq__(role_id))
            .first()
        )
        if db_user_has_role:
            db.delete(db_user_has_role)
            db.commit()
        return db_user_has_role
