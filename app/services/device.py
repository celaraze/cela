from app.database import crud, schemas, tables


def get_user_has_devices(db, device_id: int):
    conditions = [
        schemas.QueryForm(key="device_id", operator="==", value=device_id),
    ]
    return crud.selects(db, tables.UserHasDevice, conditions)


def get_users(db, device_id: int):
    user_has_devices = get_user_has_devices(db, device_id)
    users = []
    for user_has_device in user_has_devices:
        user = crud.select_id(db, tables.User, user_has_device.user_id)
        if user:
            users.append(user)
    return users


def get_current_user(db, device_id: int):
    users = get_users(db, device_id)
    for user in users:
        if user.flag in [1, 2]:
            return user
    return None
