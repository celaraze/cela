from app.database import crud, schemas, tables


def get_user_has_roles(db, role_id: int):
    conditions = [
        schemas.QueryForm(key="role_id", operator="==", value=role_id),
    ]
    return crud.selects(db, tables.UserHasRole, conditions)


def get_users(db, role_id: int):
    users = []
    user_has_roles = get_user_has_roles(db, role_id)
    for user_has_role in user_has_roles:
        user = crud.select_id(db, tables.User, user_has_role.user_id)
        if user:
            users.append(user)
    return users
