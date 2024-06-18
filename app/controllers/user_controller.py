from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, crud, tables
from ..utils import crypt, common
from ..services.user import get_roles, get_devices

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# APIs for user.

# Get all users.
@router.get("/")
async def get_users(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["user:list"]),
):
    users = crud.select_all(db, tables.User, skip=skip, limit=limit)
    return users


# Get all trashed users.
# Reserved for admin.
@router.get("/trashed")
async def get_users_trashed(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["user:list", "trashed:list"]),
):
    users = crud.select_all_with_trashed(db, tables.User, skip=skip, limit=limit)
    return users


# Get user by id.
@router.get("/{user_id}")
async def get_user(
        db: databaseSession,
        user_id: int = None,
        current_user: schemas.User = Security(get_current_user, scopes=["user:info"]),
):
    user = crud.select_id(db, tables.User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    user.roles = get_roles(db, user.id)
    user.devices = get_devices(db, user.id)
    return user


# Get trashed user by id.
# Reserved for admin.
@router.get("/{user_id}/trashed")
async def get_user_trashed(
        db: databaseSession,
        user_id: int = None,
        current_user: schemas.User = Security(get_current_user, scopes=["user:info", "trashed:info"]),
):
    user = crud.select_id(db, tables.User, user_id, with_trashed=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    return user


# Create user.
@router.post("/", response_model=schemas.User)
async def create_user(
        db: databaseSession,
        form_data: schemas.UserCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user:create"]),
):
    db_user = crud.select_email(db, tables.User, form_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )
    db_user = crud.select_username(db, tables.User, form_data.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    form_data.creator_id = current_user.id
    db_user = crud.create_user(db, tables.User, form_data)
    return db_user


# Update user.
@router.put("/{user_id}")
async def update_user(
        db: databaseSession,
        user_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["user:update"]),
):
    db_user = crud.select_id(db, tables.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    for i, form in form_data:
        if form.key not in ["username", "name", "email", "password"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ony username, name, email and password can be updated",
            )
        if form.key == "password":
            form.key = "hashed_password"
            form.value = crypt.hash_password(form.value)
            form_data[i] = form
    db_user = crud.update(db, tables.User, db_user.id, form_data)
    return db_user


# Soft delete user.
@router.delete("/{user_id}")
async def delete_user(
        db: databaseSession,
        user_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user:delete"]),
):
    db_user = crud.select_id(db, tables.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    # Delete user has roles and user has devices.
    conditions = [schemas.QueryForm(key="user_id", operator="==", value=user_id)]
    crud.delete_conditions(db, tables.UserHasRole, conditions)
    crud.delete_conditions(db, tables.UserHasDevice, conditions)
    db_user = crud.delete(db, tables.User, user_id)
    return db_user


# Restore user.
# Reserved for admin.
@router.put("/{user_id}/restore")
async def restore_user(
        db: databaseSession,
        user_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user:restore", "trashed:restore"]),
):
    db_user = crud.select_id(db, tables.User, user_id, with_trashed=True)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    db_user = crud.restore(db, tables.User, user_id)
    return db_user


# API for user has role.

# Get all user's roles.
@router.get("/{user_id}/roles")
async def get_user_roles(
        db: databaseSession,
        user_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:list"]),
):
    user_roles = get_roles(db, user_id)
    return user_roles


# Create user's role.
@router.post("/{user_id}/roles")
async def create_user_role(
        db: databaseSession,
        user_id: int,
        form_data: schemas.UserHasRoleCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:create"]),
):
    if user_id != form_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User id mismatch",
        )
    db_user = crud.select_id(db, tables.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    db_role = crud.select_id(db, tables.Role, form_data.role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists",
        )
    db_user_has_role = crud.selects(db, tables.UserHasRole, [
        schemas.QueryForm(key="user_id", operator="==", value=user_id),
        schemas.QueryForm(key="role_id", operator="==", value=form_data.role_id),
    ])
    if db_user_has_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User role already exists",
        )
    db_user_has_role = crud.create(db, tables.UserHasRole, form_data)
    return db_user_has_role


# Delete user's role.
@router.delete("/{user_id}/roles/{role_id}")
async def delete_user_role(
        db: databaseSession,
        user_id: int,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:delete"]),
):
    db_user_has_role = crud.selects(db, tables.UserHasRole, [
        schemas.QueryForm(key="user_id", operator="==", value=user_id),
        schemas.QueryForm(key="role_id", operator="==", value=role_id),
    ])
    if not db_user_has_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists",
        )
    return crud.delete_conditions(db, tables.UserHasRole, [
        schemas.QueryForm(key="user_id", operator="==", value=user_id),
        schemas.QueryForm(key="role_id", operator="==", value=role_id),
    ])


# API for user has device.

# Get all user's devices.
@router.get("/{user_id}/devices")
async def get_user_devices(
        db: databaseSession,
        user_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_device:list"]),
):
    user_devices = get_devices(db, user_id)
    return user_devices


# Create user's device.
@router.post("/{user_id}/devices")
async def create_user_device(
        db: databaseSession,
        user_id: int,
        form_data: schemas.UserHasDeviceCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_device:create"]),
):
    if user_id != form_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User id mismatch",
        )
    db_user = crud.select_id(db, tables.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    db_device = crud.select_id(db, tables.Device, form_data.device_id)
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists",
        )
    db_user_has_device = crud.selects(db, tables.UserHasDevice, [
        schemas.QueryForm(key="user_id", operator="==", value=user_id),
        schemas.QueryForm(key="device_id", operator="==", value=form_data.device_id),
    ])
    if db_user_has_device:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User device already exists",
        )
    db_user_has_device = crud.create(db, tables.UserHasDevice, form_data)
    return db_user_has_device


# Delete user's device.
# User return device.
@router.delete("/{user_id}/devices/{device_id}")
async def delete_user_device(
        db: databaseSession,
        user_id: int,
        device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_device:delete"]),
):
    db_user_has_devices = crud.selects(db, tables.UserHasDevice, [
        schemas.QueryForm(key="user_id", operator="==", value=user_id),
        schemas.QueryForm(key="device_id", operator="==", value=device_id),
    ])
    if not db_user_has_devices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User device not exists",
        )
    # Clone a new record and soft delete old record.
    new_db_user_has_device = crud.copy_and_soft_delete_old(db, tables.UserHasDevice, db_user_has_devices[0])
    # Update flag to -1. It means user has returned the device.
    update_form = [
        schemas.UpdateForm(key="flag", value=-1),
        schemas.UpdateForm(key="returned_at", value=common.now()),
    ]
    # Delete the new record.
    new_db_user_has_device = crud.update(db, tables.UserHasDevice, new_db_user_has_device.id, update_form)
    return crud.delete(db, tables.UserHasDevice, new_db_user_has_device[0].id)
