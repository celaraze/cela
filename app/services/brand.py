from sqlalchemy import select

from app.database import tables


def get_devices(db, brand):
    stmt = (
        select(tables.Device)
        .where(tables.Device.deleted_at.is_(None))
        .where(tables.Device.brand_id.__eq__(brand.id))

    )
    devices = db.scalars(stmt).all()
    return devices
