from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, crud, tables
from ..services.device import get_user

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# APIs for device.

# Get all devices.
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


# Get device by id.
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
    user = get_user(db, device_id)
    device.user = user
    return device


# Create device.
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


# Update device.
@router.put("/{device_id}")
async def update_device(
        db: databaseSession,
        device_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["device:update"]),
):
    db_device = crud.select_id(db, tables.Device, device_id)
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists",
        )
    for form in form_data:
        if form.key == "brand_id":
            db_brand = crud.select_id(db, tables.Brand, form.value)
            if not db_brand:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Brand not exists",
                )
        elif form.key == "category_id":
            db_device_category = crud.select_id(db, tables.DeviceCategory, form.value)
            if not db_device_category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Device category not exists",
                )
        elif form.key == "asset_number":
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Asset number cannot be updated",
            )
        else:
            continue
    db_device = crud.update(db, tables.Device, device_id, form_data)
    return db_device


# Delete device.
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
    users = get_user(db, device_id)
    if users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device has users, please update them first.",
        )
    db_brand = crud.delete(db, tables.Device, device_id)
    return db_brand
