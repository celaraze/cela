from fastapi import APIRouter, HTTPException, status, Security
from sqlalchemy import select

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..utils import crypt, common
from ..services.device import returned

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# APIs for user.

# Get all users.
@router.get("/", response_model=list[schemas.User])
async def get_users(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["user:list"]),
):
    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.isnot(None))
        .offset(skip)
        .limit(limit)
    )
    users = db.scalars(stmt).all()
    return users


# Get user by id.
@router.get("/{user_id}", response_model=schemas.User)
async def get_user(
        db: databaseSession,
        user_id: int = None,
        current_user: schemas.User = Security(get_current_user, scopes=["user:info"]),
):
    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.isnot(None))
        .where(tables.User.id.__eq__(user_id))
    )
    user = db.scalars(stmt).one_or_none()
    user.roles = user.roles
    user.devices = user.devices
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists.",
        )
    return user


# Create user.
@router.post("/", response_model=schemas.User)
async def create_user(
        db: databaseSession,
        form_data: schemas.UserCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user:create"]),
):
    if form_data.username == "admin":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username name 'admin' is reserved.",
        )
    # The email is always unique, so we don't need to filter soft deleted records.
    stmt = (
        select(tables.User)
        .where(tables.User.email.__eq__(form_data.email))
    )
    db_user = db.scalars(stmt).one_or_none()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        )
    # The username is always unique, so we don't need to filter soft deleted records.
    stmt = (
        select(tables.User)
        .where(tables.User.username.__eq__(form_data.username))
    )
    db_user = db.scalars(stmt).one_or_none()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists.",
        )
    form_data.creator_id = current_user.id
    form_data.hashed_password = crypt.hash_password(form_data.password)
    form_data.pop("password")
    user = tables.User(**form_data.dict())
    db.add(user)
    return user


# Update user.
@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
        db: databaseSession,
        user_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["user:update"]),
):
    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.isnot(None))
        .where(tables.User.id.__eq__(user_id))
    )
    db_user = db.scalars(stmt).one_or_none()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists.",
        )
    for form in form_data:
        if form.key not in ["username", "name", "email", "password"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ony username, name, email and password can be updated",
            )
        if form.key == "password":
            form.key = "hashed_password"
            form.value = crypt.hash_password(form.value)
        if (form.key == "username") and (form.value == "admin"):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username name 'admin' is reserved.",
            )
        setattr(db_user, form.key, form.value)
    db.commit()
    return db_user


# Soft delete user.
@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(
        db: databaseSession,
        user_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user:delete"]),
):
    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.isnot(None))
        .where(tables.User.id.__eq__(user_id))
    )
    user = db.scalars(stmt).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists.",
        )
    if user.username == "admin":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username name 'admin' is reserved.",
        )
    # Delete user has roles and user has devices.
    for role in user.roles:
        stmt = (
            select(tables.user_has_roles_table)
            .where(tables.user_has_roles_table.c.user_id.__eq__(user_id))
            .where(tables.user_has_roles_table.c.role_id.__eq__(role.id))
        )
        user_has_role = db.scalars(stmt).one_or_none()
        if user_has_role:
            setattr(user_has_role, "deleted_at", common.now())
        db.commit()

    for device in user.devices:
        stmt = (
            select(tables.user_has_devices_table)
            .where(tables.user_has_devices_table.c.user_id.__eq__(user_id))
            .where(tables.user_has_devices_table.c.device_id.__eq__(device.id))
        )
        user_has_device = db.scalars(stmt).one_or_none()
        if user_has_device:
            setattr(user_has_device, "deleted_at", common.now())
        db.commit()

    setattr(user, "deleted_at", common.now())
    db.commit()
    return user


# API for user has role.

# Create user's role.
@router.post("/{user_id}/roles", response_model=schemas.UserHasRole)
async def create_user_role(
        db: databaseSession,
        user_id: int,
        form_data: schemas.UserHasRoleCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:create"]),
):
    if user_id != form_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User id mismatch.",
        )
    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.isnot(None))
        .where(tables.User.id.__eq__(user_id))
    )
    user = db.scalars(stmt).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists.",
        )
    stmt = (
        select(tables.Role)
        .where(tables.Role.deleted_at.isnot(None))
        .where(tables.Role.id.__eq__(form_data.role_id))
    )
    role = db.scalars(stmt).one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists.",
        )

    if role in user.roles:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has this role.",
        )

    user.roles.append(role)
    db.commit()

    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Create user has role successfully.",
    )


# Delete user's role.
@router.delete("/{user_id}/roles/{role_id}", response_model=list[schemas.UserHasRole])
async def delete_user_role(
        db: databaseSession,
        user_id: int,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:delete"]),
):
    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.isnot(None))
        .where(tables.User.id.__eq__(user_id))
    )
    user = db.scalars(stmt).one_or_none()

    stmt = (
        select(tables.Role)
        .where(tables.Role.deleted_at.isnot(None))
        .where(tables.Role.id.__eq__(role_id))
    )
    role = db.scalars(stmt).one_or_none()

    if (user and (user.username == "admin")) and (role and (role.name == "superuser")):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Superuser role cannot be deleted from admin user.",
        )

    user.roles.remove(role)
    db.commit()

    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Delete user has role successfully.",
    )


# API for user has device.

# Create user's device.
@router.post("/{user_id}/devices/out", response_model=schemas.UserHasDevice)
async def create_user_device(
        db: databaseSession,
        user_id: int,
        form_data: schemas.UserHasDeviceCreateOrUpdateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_device:create"]),
):
    if user_id != form_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User id mismatch.",
        )

    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.isnot(None))
        .where(tables.User.id.__eq__(user_id))
    )
    user = db.scalars(stmt).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists.",
        )

    stmt = (
        select(tables.Device)
        .where(tables.Device.deleted_at.isnot(None))
        .where(tables.Device.id.__eq__(form_data.device_id))
    )
    device = db.scalars(stmt).one_or_none()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists.",
        )

    if device in user.devices:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User device already exists.",
        )

    user.devices.append(device)
    db.commit()

    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Create user has device successfully.",
    )


# Return user's device.
@router.post("/{user_id}/devices/in")
async def delete_user_device(
        db: databaseSession,
        user_id: int,
        form_data: schemas.UserHasDeviceCreateOrUpdateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_device:delete"]),
):
    if user_id != form_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User id mismatch.",
        )

    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.isnot(None))
        .where(tables.User.id.__eq__(user_id))
    )
    user = db.scalars(stmt).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists.",
        )

    stmt = (
        select(tables.Device)
        .where(tables.Device.deleted_at.isnot(None))
        .where(tables.Device.id.__eq__(form_data.device_id))
    )
    device = db.scalars(stmt).one_or_none()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists.",
        )

    if device not in user.devices:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User device not exists.",
        )

    result = returned(db, user, device, current_user.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Device is locked.",
        )
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Device returned.",
    )
