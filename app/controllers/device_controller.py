from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..services.device import get_user
from ..utils import common

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# APIs for device.

# Get all devices.
@router.get("/", response_model=list[schemas.Device])
async def get_devices(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        asset_number: str = None,
        current_user: schemas.User = Security(get_current_user, scopes=["device:list"]),
):
    db_query = (
        db.query(tables.Device)
        .filter(tables.Device.deleted_at.isnot(None))
        .offset(skip)
        .limit(limit)
    )
    if asset_number:
        db_query = db_query.filter(tables.Device.asset_number == asset_number)
    devices = db_query.all()
    return devices


# Get device by id.
@router.get("/{device_id}", response_model=schemas.Device)
async def get_device(
        db: databaseSession,
        device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device:info"]),
):
    device = (
        db.query(tables.Device)
        .filter(tables.Device.deleted_at.isnot(None))
        .filter(tables.Device.id == device_id)
        .first()
    )
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists.",
        )
    device.creator = (
        db.query(tables.User)
        .filter(tables.User.id == device.creator_id)
        .first()
    )
    user = get_user(db, device_id)
    device.user = user
    return device


# Create device.
@router.post("/", response_model=schemas.Device)
async def create_device(
        db: databaseSession,
        form_data: schemas.DeviceCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["device:create"]),
):
    # The asset number is always unique, so we don't need to filter soft deleted records.
    db_device = (
        db.query(tables.Device)
        .filter(tables.Device.asset_number == form_data.asset_number)
        .first()
    )
    if db_device:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device asset number already exists.",
        )
    db_brand = (
        db.query(tables.Brand)
        .filter(tables.Brand.deleted_at.isnot(None))
        .filter(tables.Brand.id == form_data.brand_id)
        .first()
    )
    if not db_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists.",
        )
    db_device_category = (
        db.query(tables.DeviceCategory)
        .filter(tables.DeviceCategory.deleted_at.isnot(None))
        .filter(tables.DeviceCategory.id == form_data.category_id)
        .first()
    )
    if not db_device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device category not exists.",
        )
    form_data.creator_id = current_user.id
    device = tables.Device(**form_data.dict())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


# Update device.
@router.put("/{device_id}", response_model=schemas.Device)
async def update_device(
        db: databaseSession,
        device_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["device:update"]),
):
    db_device = (
        db.query(tables.Device)
        .filter(tables.Device.deleted_at.isnot(None))
        .filter(tables.Device.id == device_id)
        .first()
    )
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists.",
        )
    for form in form_data:
        if form.key == "brand_id":
            db_brand = (
                db.query(tables.Brand)
                .filter(tables.Brand.deleted_at.isnot(None))
                .filter(tables.Brand.id == form.value)
                .first()
            )
            if not db_brand:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Brand not exists.",
                )
        elif form.key == "category_id":
            db_device_category = (
                db.query(tables.DeviceCategory)
                .filter(tables.DeviceCategory.deleted_at.isnot(None))
                .filter(tables.DeviceCategory.id == form.value)
                .first()
            )
            if not db_device_category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Device category not exists.",
                )
        elif form.key == "asset_number":
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Asset number cannot be updated.",
            )
        else:
            continue
    for form in form_data:
        setattr(db_device, form.key, form.value)
    db.commit()
    db.refresh(db_device)
    return db_device


# Delete device.
@router.delete("/{device_id}", response_model=schemas.Device)
async def delete_device(
        db: databaseSession,
        device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device:delete"]),
):
    db_device = (
        db.query(tables.Device)
        .filter(tables.Device.deleted_at.isnot(None))
        .filter(tables.Device.id == device_id)
        .first()
    )
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists.",
        )
    users = get_user(db, device_id)
    if users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device has users, please update them first.",
        )
    setattr(db_device, "deleted_at", common.now())
    db.commit()
    db.refresh(db_device)
    return db_device
