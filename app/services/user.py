from app.utils import common
from sqlalchemy import select, alias
from sqlalchemy.orm import aliased

from app.database import tables, schemas


def get_devices(db, user):
    stmt = (
        select(tables.Device, tables.UserHasDevice)
        .join(tables.UserHasDevice, tables.Device.id == tables.UserHasDevice.device_id)
        .join(tables.User, tables.User.id == tables.UserHasDevice.user_id)
        .where(tables.UserHasDevice.deleted_at.is_(None))
        .where(tables.Device.deleted_at.is_(None))
        .where(tables.UserHasDevice.user_id.__eq__(user.id))
    )
    devices = db.scalars(stmt).all()
    return devices


# Get historical devices.
def get_historical_devices(db, user):
    stmt = (
        select(tables.UserHasDevice, tables.Device, tables.User)
        .join(tables.Device, tables.Device.id == tables.UserHasDevice.device_id)
        .join(tables.User, tables.User.id == tables.UserHasDevice.user_id)
        .where(tables.UserHasDevice.deleted_at.isnot(None))
        .where(tables.UserHasDevice.user_id.__eq__(user.id))
    )
    historical_devices = []
    user_has_devices = db.execute(stmt).all()
    for user_has_device in user_has_devices:
        user_has_device_table = user_has_device[0]
        device_table = user_has_device[1]
        creator = common.get_creator(db, user_has_device_table.creator_id)
        creator = schemas.Creator(**creator.__dict__)
        historical_device = schemas.UserHistoricalDevice(
            id=user_has_device_table.id,
            device_id=user_has_device_table.device_id,
            device_hostname=device_table.hostname,
            device_asset_number=device_table.asset_number,
            device_description=device_table.description,
            creator=creator,
            created_at=user_has_device_table.created_at,
            deleted_at=user_has_device_table.deleted_at,
        )
        historical_devices.append(historical_device)
    return historical_devices


def get_roles(db, user):
    stmt = (
        select(tables.Role, tables.UserHasRole)
        .join(tables.UserHasRole, tables.Role.id == tables.UserHasRole.role_id)
        .join(tables.User, tables.User.id == tables.UserHasRole.user_id)
        .where(tables.UserHasRole.deleted_at.is_(None))
        .where(tables.Role.deleted_at.is_(None))
        .where(tables.UserHasRole.user_id.__eq__(user.id))
    )

    roles = db.scalars(stmt).all()
    return roles


# Get historical roles.
def get_historical_roles(db, user):
    stmt = (
        select(tables.UserHasRole, tables.Role, tables.User)
        .join(tables.Role, tables.Role.id == tables.UserHasRole.role_id)
        .join(tables.User, tables.User.id == tables.UserHasRole.user_id)
        .where(tables.UserHasRole.deleted_at.isnot(None))
        .where(tables.UserHasRole.user_id.__eq__(user.id))
    )
    historical_roles = []
    user_has_roles = db.execute(stmt).all()
    for user_has_role in user_has_roles:
        user_has_role_table = user_has_role[0]
        role_table = user_has_role[1]
        creator = common.get_creator(db, user_has_role_table.creator_id)
        creator = schemas.Creator(**creator.__dict__)
        historical_role = schemas.UserHistoricalRole(
            id=user_has_role_table.id,
            role_id=user_has_role_table.role_id,
            role_name=role_table.name,
            role_scopes=role_table.scopes,
            creator=creator,
            created_at=user_has_role_table.created_at,
            deleted_at=user_has_role_table.deleted_at,
        )
        historical_roles.append(historical_role)
    return historical_roles
