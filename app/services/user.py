from app.database import crud, schemas, tables


def get_user_has_roles(db, user_id: int):
    conditions = [
        schemas.QueryForm(key="user_id", operator="==", value=user_id),
    ]
    return crud.selects(db, tables.UserHasRole, conditions)


def get_roles(db, user_id: int):
    roles = []
    user_has_roles = get_user_has_roles(db, user_id)
    for user_has_role in user_has_roles:
        role = crud.select_id(db, tables.Role, user_has_role.role_id)
        if role:
            roles.append(role)
    return roles


def get_scopes(db, user_id: int):
    roles = get_roles(db, user_id)
    scopes = []
    for role in roles:
        scopes.extend(role.scopes)
    return scopes
