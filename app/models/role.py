from sqlalchemy.orm import Session

from ..database import tables, schemas


class Role:
    @staticmethod
    def select_one(db: Session, role_id: int):
        return (
            db.query(tables.Role)
            .filter(tables.Role.id.__eq__(role_id))
            .first()
        )

    @staticmethod
    def select_one_by_name(db: Session, name: str):
        return (
            db.query(tables.Role)
            .filter(tables.Role.name.__eq__(name))
            .first()
        )

    @staticmethod
    def select_all(db: Session, skip: int = 0, limit: int = 100):
        return (
            db.query(tables.Role)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, role: schemas.RoleForm) -> tables.Role:
        role_dict = role.model_dump()
        db_role = tables.Role(
            **role_dict,
        )
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role

    @staticmethod
    def update(db: Session, role: schemas.Role, form_data: schemas.UpdateForm):
        db_role = (
            db.query(tables.Role)
            .filter(tables.Role.id.__eq__(role.id))
            .first()
        )
        if db_role:
            setattr(db_role, form_data.key, form_data.value)
            db.commit()
            db.refresh(db_role)
        return db_role

    @staticmethod
    def delete(db: Session, role_id: int):
        db_role = (
            db.query(tables.Role)
            .filter(tables.Role.id.__eq__(role_id))
            .first()
        )
        if db_role:
            db.delete(db_role)
            db.commit()
        return db_role
