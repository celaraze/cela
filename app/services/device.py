from app.utils import common
from sqlalchemy import select

from app.database import tables, schemas


def get_user(db, device):
    stmt = (
        select(tables.User, tables.UserHasDevice)
        .join(tables.UserHasDevice, tables.User.id == tables.UserHasDevice.user_id)
        .join(tables.Device, tables.Device.id == tables.UserHasDevice.device_id)
        .where(tables.UserHasDevice.deleted_at.is_(None))
        .where(tables.User.deleted_at.is_(None))
        .where(tables.UserHasDevice.device_id.__eq__(device.id))
    )
    user = db.scalars(stmt).one_or_none()
    return user


# Get historical users.
def get_historical_users(db, device):
    stmt = (
        select(tables.UserHasDevice, tables.User, tables.Device)
        .join(tables.User, tables.User.id == tables.UserHasDevice.user_id)
        .join(tables.Device, tables.Device.id == tables.UserHasDevice.device_id)
        .where(tables.UserHasDevice.deleted_at.isnot(None))
        .where(tables.UserHasDevice.device_id.__eq__(device.id))
    )
    historical_users = []
    user_has_devices = db.execute(stmt).all()
    for user_has_device in user_has_devices:
        user_has_device_table = user_has_device[0]
        user_table = user_has_device[1]
        creator = common.get_creator(db, user_has_device_table.creator_id)
        creator = schemas.Creator(**creator.__dict__)
        historical_user = schemas.DeviceHistoricalUser(
            id=user_has_device_table.id,
            user_id=user_has_device_table.user_id,
            user_name=user_table.name,
            user_username=user_table.scopes,
            user_email=user_table.email,
            creator=creator,
            created_at=user_has_device_table.created_at,
            deleted_at=user_has_device_table.deleted_at,
        )
        historical_users.append(historical_user)
    return historical_users


def get_brand(db, device):
    stmt = (
        select(tables.Brand)
        .where(tables.Brand.deleted_at.is_(None))
        .where(tables.Brand.id.__eq__(device.brand_id))
    )
    brand = db.scalars(stmt).one_or_none()
    return brand


def get_category(db, device):
    stmt = (
        select(tables.DeviceCategory)
        .where(tables.DeviceCategory.deleted_at.is_(None))
        .where(tables.DeviceCategory.id.__eq__(device.category_id))
    )
    category = db.scalars(stmt).one_or_none()
    return category
