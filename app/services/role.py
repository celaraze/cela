from sqlalchemy import select

from app.database import tables


def get_users(db, role):
    stmt = (
        select(tables.User)
        .join(tables.UserHasRole, tables.User.id == tables.UserHasRole.user_id)
        .join(tables.Role, tables.Role.id == tables.UserHasRole.role_id)
        .where(tables.UserHasRole.deleted_at.is_(None))
        .where(tables.User.deleted_at.is_(None))
        .where(tables.UserHasRole.role_id.__eq__(role.id))
    )
    users = db.scalars(stmt).all()
    return users
