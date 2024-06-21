from app.utils import common
from sqlalchemy import select

from app.database import tables, schemas


def get_users(db, role):
    stmt = (
        select(tables.User, tables.UserHasRole)
        .join(tables.UserHasRole, tables.User.id == tables.UserHasRole.user_id)
        .join(tables.Role, tables.Role.id == tables.UserHasRole.role_id)
        .where(tables.UserHasRole.deleted_at.is_(None))
        .where(tables.User.deleted_at.is_(None))
        .where(tables.UserHasRole.role_id.__eq__(role.id))
    )
    users = db.scalars(stmt).all()
    return users


# Get historical users.
def get_historical_users(db, role):
    stmt = (
        select(tables.UserHasRole, tables.User, tables.Role)
        .join(tables.User, tables.User.id == tables.UserHasRole.user_id)
        .join(tables.Role, tables.Role.id == tables.UserHasRole.role_id)
        .where(tables.UserHasRole.deleted_at.isnot(None))
        .where(tables.UserHasRole.role_id.__eq__(role.id))
    )
    historical_users = []
    user_has_roles = db.execute(stmt).all()
    for user_has_role in user_has_roles:
        user_has_role_table = user_has_role[0]
        user_table = user_has_role[1]
        creator = common.get_creator(db, user_has_role_table.creator_id)
        creator = schemas.Creator(**creator.__dict__)
        historical_user = schemas.RoleHistoricalUser(
            id=user_has_role_table.id,
            user_id=user_has_role_table.user_id,
            user_name=user_table.name,
            user_username=user_table.scopes,
            user_email=user_table.email,
            creator=creator,
            created_at=user_has_role_table.created_at,
            deleted_at=user_has_role_table.deleted_at,
        )
        historical_users.append(historical_user)
    return historical_users
