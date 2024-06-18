from app.database import crud, schemas, tables
from app.utils import common


def get_user_has_device(db, device_id: int):
    conditions = [
        schemas.QueryForm(key="device_id", operator="==", value=device_id),
        schemas.QueryForm(key="status", operator="==", value=0),
    ]
    user_has_devices = crud.selects(db, tables.UserHasDevice, conditions)
    if not user_has_devices:
        return None
    return user_has_devices[0]


def get_user(db, device_id):
    user_has_device = get_user_has_device(db, device_id)
    if not user_has_device:
        return None
    if user_has_device.flag == -1:
        return None
    user = crud.select_id(db, tables.User, user_has_device.user_id)
    if not user:
        return None
    return user


def returned(
        db,
        table,
        old_db_record,
        creator_id,
):
    new_db_record = crud.copy(db, table, old_db_record)
    if new_db_record:
        update_form = [
            schemas.UpdateForm(key="flag", value=-1),
            schemas.UpdateForm(key="status", value=1),
            schemas.UpdateForm(key="creator_id", value=creator_id),
            schemas.UpdateForm(key="created_at", value=common.now()),
        ]
        crud.update(db, table, new_db_record.id, update_form)
        crud.update(db, table, old_db_record.id, update_form)
        return True
    return False
