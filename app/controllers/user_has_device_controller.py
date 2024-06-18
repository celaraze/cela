from fastapi import APIRouter, HTTPException, status, Security

from ..database import schemas, crud, tables
from ..dependencies import get_oauth_scheme, get_current_user, databaseSession

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/user_has_devices",
    tags=["user_has_devices"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_user_has_devices(
        db: databaseSession,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_device:list"]),
        skip: int = 0,
        limit: int = 100,
):
    user_has_devices = crud.select_all(db, tables.UserHasDevice, skip=skip, limit=limit)
    if not user_has_devices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User devices not exists",
        )
    return user_has_devices


@router.get("/{user_has_device_id}")
async def get_user_has_device(
        db: databaseSession,
        user_has_device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_device:info"]),
):
    user_has_device = crud.select_id(db, tables.UserHasDevice, user_has_device_id)
    if not user_has_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User device not exists",
        )
    return user_has_device


@router.post("/")
async def create_user_has_device(
        db: databaseSession,
        form_data: schemas.UserHasDeviceCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_device:create"]),
):
    db_user = crud.select_id(db, tables.User, form_data.user_id)
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
    conditions = [
        schemas.QueryForm(key="user_id", operator="==", value=form_data.user_id),
        schemas.QueryForm(key="device_id", operator="==", value=form_data.device_id),
    ]
    db_user_has_devices = crud.selects(db, tables.UserHasDevice, conditions)
    if db_user_has_devices:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User device already exists",
        )
    form_data.creator_id = current_user.id
    db_user_has_device = crud.create(db, tables.UserHasDevice, form_data)
    return db_user_has_device


# todo update_user_has_device
@router.put("/{user_has_device_id}")
async def update_user_has_device(
        db: databaseSession,
        user_has_device_id: int,
        form_data: schemas.UpdateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_device:update"]),
):
    pass


@router.delete("/{user_has_device_id}")
async def delete_user_has_device(
        db: databaseSession,
        user_has_device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_device:delete"]),
):
    db_user_has_device = crud.select_id(db, tables.UserHasDevice, user_has_device_id)
    if not db_user_has_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User device not exists",
        )
    db_user_has_device = crud.delete(db, tables.UserHasDevice, user_has_device_id)
    return db_user_has_device


@router.delete("/")
async def delete_user_has_role_by_user_id_and_role_id(
        db: databaseSession,
        user_id: int,
        device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_device:delete"]),
):
    conditions = [
        schemas.QueryForm(key="user_id", operator="==", value=user_id),
        schemas.QueryForm(key="device_id", operator="==", value=device_id),
    ]
    db_user_has_devices = crud.selects(db, tables.UserHasDevice, conditions)
    if not db_user_has_devices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User device not exists",
        )
    db_user_has_device = crud.delete(db, tables.UserHasDevice, db_user_has_devices[0].id)
    return db_user_has_device
