from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, crud, tables

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_devices(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        asset_number: str = None,
        current_user: schemas.User = Security(get_current_user, scopes=["device:list"]),
):
    devices = crud.select_all(db, tables.Device, skip=skip, limit=limit)
    if asset_number:
        devices = crud.select_asset_number(db, tables.Device, asset_number)
    return devices


@router.get("/{device_id}")
async def get_device(
        db: databaseSession,
        device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device:info"]),
):
    device = crud.select_id(db, tables.Device, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists",
        )
    return device


@router.post("/")
async def create_device(
        db: databaseSession,
        form_data: schemas.DeviceCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["device:create"]),
):
    db_device = crud.select_asset_number(db, tables.Device, form_data.asset_number)
    if db_device:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device asset number already exists",
        )
    db_brand = crud.select_id(db, tables.Brand, form_data.brand_id)
    if not db_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists",
        )
    db_device_category = crud.select_id(db, tables.DeviceCategory, form_data.category_id)
    if not db_device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device category not exists",
        )
    form_data.creator_id = current_user.id
    db_device = crud.create(db, tables.Device, form_data)
    return db_device


@router.put("/{device_id}")
async def update_device(
        db: databaseSession,
        device_id: int,
        form_data: schemas.UpdateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["device:update"]),
):
    db_device = crud.select_id(db, tables.Device, device_id)
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists",
        )
    if form_data.key == "asset_number":
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Asset number cannot be updated",
        )
    db_device = crud.update(db, tables.Device, device_id, form_data)
    return db_device


@router.delete("/{device_id}")
async def delete_device(
        db: databaseSession,
        device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device:delete"]),
):
    db_device = crud.select_id(db, tables.Device, device_id)
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists",
        )
    db_brand = crud.delete(db, tables.Device, device_id)
    return db_brand
