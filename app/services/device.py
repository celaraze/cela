from app.database import crud, schemas, tables


def get_user_has_device(db, device_id: int):
    conditions = [
        schemas.QueryForm(key="device_id", operator="==", value=device_id),
    ]
    user_has_devices = crud.selects(db, tables.UserHasDevice, conditions)
    return user_has_devices[0]


def get_user(db, device_id):
    user_id = get_user_has_device(db, device_id)
    user = crud.select_id(db, tables.User, user_id)
    if not user:
        return None
    return user
