from sqlalchemy import select

from app.database import tables


def get_users(db, device):
    stmt = (
        select(tables.User)
        .join(tables.UserHasDevice, tables.User.id == tables.UserHasDevice.user_id)
        .join(tables.Device, tables.Device.id == tables.UserHasDevice.device_id)
        .where(tables.UserHasDevice.deleted_at.is_(None))
        .where(tables.User.deleted_at.is_(None))
        .where(tables.UserHasDevice.device_id.__eq__(device.id))
    )
    users = db.scalars(stmt).all()
    return users


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
