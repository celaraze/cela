from fastapi import APIRouter, HTTPException, status, Security
from sqlalchemy import select

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
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
@router.get("/", response_model=list[schemas.User])
async def get_users(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["user:list"]),
):
    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.is_(None))
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
        .where(tables.User.deleted_at.is_(None))
        .where(tables.User.id.__eq__(user_id))
    )
    user = db.scalars(stmt).one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists.",
        )
    user.creator = common.get_creator(db, user.creator_id)
    user.roles = get_roles(db, user)
    user.devices = get_devices(db, user)

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
    user = db.scalars(stmt).one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        )
    # The username is always unique, so we don't need to filter soft deleted records.
    stmt = (
        select(tables.User)
        .where(tables.User.username.__eq__(form_data.username))
    )
    user = db.scalars(stmt).one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists.",
        )
    form_data.creator_id = current_user.id
    form_data.hashed_password = crypt.hash_password(form_data.password)
    del form_data.password
    user = tables.User(**form_data.model_dump())
    db.add(user)
    db.commit()
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
        .where(tables.User.deleted_at.is_(None))
        .where(tables.User.id.__eq__(user_id))
    )
    user = db.scalars(stmt).one_or_none()
    if not user:
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
        setattr(user, form.key, form.value)
    db.commit()
    return user


# Soft delete user.
@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(
        db: databaseSession,
        user_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user:delete"]),
):
    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.is_(None))
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

    stmt = (
        select(tables.UserHasRole)
        .where(tables.UserHasRole.deleted_at.is_(None))
        .where(tables.UserHasRole.user_id.__eq__(user_id))
    )

    user_has_roles = db.scalars(stmt).all()

    for user_has_role in user_has_roles:
        setattr(user_has_role, "deleted_at", common.now())
        db.commit()

    stmt = (
        select(tables.UserHasDevice)
        .where(tables.UserHasDevice.deleted_at.is_(None))
        .where(tables.UserHasDevice.user_id.__eq__(user_id))
    )

    user_has_devices = db.scalars(stmt).all()

    for user_has_device in user_has_devices:
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
        .where(tables.User.deleted_at.is_(None))
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
        .where(tables.Role.deleted_at.is_(None))
        .where(tables.Role.id.__eq__(form_data.role_id))
    )
    role = db.scalars(stmt).one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists.",
        )

    stmt = (
        select(tables.UserHasRole)
        .where(tables.UserHasRole.deleted_at.is_(None))
        .where(tables.UserHasRole.user_id.__eq__(user_id))
        .where(tables.UserHasRole.role_id.__eq__(form_data.role_id))
    )

    user_has_role = db.scalars(stmt).one_or_none()

    if user_has_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has this role.",
        )

    form_data.creator_id = current_user.id
    user_has_role = tables.UserHasRole(**form_data.model_dump())
    db.add(user_has_role)
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
        .where(tables.User.deleted_at.is_(None))
        .where(tables.User.id.__eq__(user_id))
    )
    user = db.scalars(stmt).one_or_none()

    stmt = (
        select(tables.Role)
        .where(tables.Role.deleted_at.is_(None))
        .where(tables.Role.id.__eq__(role_id))
    )
    role = db.scalars(stmt).one_or_none()

    if (user and (user.username == "admin")) and (role and (role.name == "superuser")):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Superuser role cannot be deleted from admin user.",
        )

    stmt = (
        select(tables.UserHasRole)
        .where(tables.UserHasRole.user_id.__eq__(user_id))
        .where(tables.UserHasRole.role_id.__eq__(role_id))
    )
    user_has_role = db.scalars(stmt).one_or_none()
    if not user_has_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists.",
        )

    setattr(user_has_role, "deleted_at", common.now())
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
    if form_data.flag not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Flag must be 1(manage) or 2(borrow).",
        )

    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.is_(None))
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
        .where(tables.Device.deleted_at.is_(None))
        .where(tables.Device.id.__eq__(form_data.device_id))
    )
    device = db.scalars(stmt).one_or_none()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists.",
        )

    stmt = (
        select(tables.UserHasDevice)
        .where(tables.UserHasDevice.deleted_at.is_(None))
        .where(tables.UserHasDevice.user_id.__eq__(user_id))
        .where(tables.UserHasDevice.device_id.__eq__(form_data.device_id))
    )

    user_has_device = db.scalars(stmt).one_or_none()

    if user_has_device:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User device already exists.",
        )

    form_data.status = 0
    form_data.creator_id = current_user.id
    form_data.created_at = common.now()

    user_has_device = tables.UserHasDevice(**form_data.model_dump())
    db.add(user_has_device)
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
        .where(tables.User.deleted_at.is_(None))
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
        .where(tables.Device.deleted_at.is_(None))
        .where(tables.Device.id.__eq__(form_data.device_id))
    )
    device = db.scalars(stmt).one_or_none()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists.",
        )

    stmt = (
        select(tables.UserHasDevice)
        .where(tables.UserHasDevice.deleted_at.is_(None))
        .where(tables.UserHasDevice.user_id.__eq__(user_id))
        .where(tables.UserHasDevice.device_id.__eq__(form_data.device_id))
    )
    user_has_devices = db.scalars(stmt).all()
    if not user_has_devices:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User device not exists.",
        )

    stmt = (
        select(tables.UserHasDevice)
        .where(tables.UserHasDevice.user_id.__eq__(user_id))
        .where(tables.UserHasDevice.device_id.__eq__(form_data.device_id))
    )

    old_user_has_device = db.scalars(stmt).one_or_none()
    if not old_user_has_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User device not exists.",
        )

    form_data = schemas.UserHasDeviceCreateOrUpdateForm(
        user_id=old_user_has_device.user_id,
        device_id=old_user_has_device.device_id,
        flag=-1,
        status=1,
        message="Returned",
        creator_id=current_user.id,
        deleted_at=common.now(),
    )

    new_user_has_device = tables.UserHasDevice(**form_data.model_dump())
    db.add(new_user_has_device)
    db.commit()

    old_user_has_device.deleted_at = common.now()
    db.commit()

    if not new_user_has_device:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Device is locked.",
        )
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Device returned.",
    )
