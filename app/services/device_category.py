from sqlalchemy import select

from app.database import tables


def get_devices(db, category):
    stmt = (
        select(tables.Device)
        .where(tables.Device.deleted_at.is_(None))
        .where(tables.Device.category_id.__eq__(category.id))

    )
    devices = db.scalars(stmt).all()
    return devices
