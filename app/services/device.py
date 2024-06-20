from sqlalchemy import select
from sqlalchemy.orm import make_transient

from app.database import schemas, tables
from app.utils import common


def returned(
        db,
        user,
        device,
        creator_id,
):
    stmt = (
        select(tables.user_has_devices_table)
        .where(tables.user_has_devices_table.deleted_at.isnot(None))
        .where(tables.user_has_devices_table.user_id.__eq__(user.id))
        .where(tables.user_has_devices_table.device_id.__eq__(device.id))
    )
    old_user_has_device = db.scalars(stmt).one_or_none()

    old_user_has_device.pop('_sa_instance_state', None)

    new_user_has_device = tables.user_has_devices_table(**old_user_has_device)
    make_transient(new_user_has_device)
    new_user_has_device.id = None
    db.add(new_user_has_device)
    db.commit()
    if new_user_has_device:
        update_form = [
            schemas.UpdateForm(key="flag", value=-1),
            schemas.UpdateForm(key="status", value=1),
            schemas.UpdateForm(key="creator_id", value=creator_id),
            schemas.UpdateForm(key="created_at", value=common.now()),
        ]
        for form in update_form:
            setattr(old_user_has_device, form.key, form.value)
            setattr(new_user_has_device, form.key, form.value)
        db.commit()
        return True
    return False
