from sqlalchemy import select

from app.database import tables


def get_devices(db, user):
    stmt = (
        select(tables.Device)
        .join(tables.UserHasDevice, tables.Device.id == tables.UserHasDevice.device_id)
        .join(tables.User, tables.User.id == tables.UserHasDevice.user_id)
        .where(tables.UserHasDevice.deleted_at.is_(None))
        .where(tables.Device.deleted_at.is_(None))
        .where(tables.UserHasDevice.user_id.__eq__(user.id))
    )
    devices = db.scalars(stmt).all()
    return devices


def get_roles(db, user):
    stmt = (
        select(tables.Role)
        .join(tables.UserHasRole, tables.Role.id == tables.UserHasRole.role_id)
        .join(tables.User, tables.User.id == tables.UserHasRole.user_id)
        .where(tables.UserHasRole.deleted_at.is_(None))
        .where(tables.Role.deleted_at.is_(None))
        .where(tables.UserHasRole.user_id.__eq__(user.id))
    )

    roles = db.scalars(stmt).all()
    return roles
