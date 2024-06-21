from fastapi import APIRouter, HTTPException, status, Security
from sqlalchemy import select

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..utils import common
from ..services.device import get_brand, get_category, get_users

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
    stmt = (
        select(tables.Device)
        .where(tables.Device.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    if asset_number:
        stmt = stmt.where(tables.Device.asset_number.__eq__(asset_number))
    devices = db.scalars(stmt).all()
    return devices


# Get device by id.
@router.get("/{device_id}", response_model=schemas.Device)
async def get_device(
        db: databaseSession,
        device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device:info"]),
):
    stmt = (
        select(tables.Device)
        .where(tables.Device.deleted_at.is_(None))
        .where(tables.Device.id.__eq__(device_id))
    )
    device = db.scalars(stmt).one_or_none()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists.",
        )
    device.creator = common.get_creator(db, device.creator_id)
    device.brand = get_brand(db, device)
    device.category = get_category(db, device)
    device.users = get_users(db, device)
    return device


# Create device.
@router.post("/", response_model=schemas.Device)
async def create_device(
        db: databaseSession,
        form_data: schemas.DeviceCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["device:create"]),
):
    # The asset number is always unique, so we don't need to filter soft deleted records.
    stmt = (
        select(tables.Device)
        .where(tables.Device.asset_number.__eq__(form_data.asset_number))
    )
    device = db.scalars(stmt).one_or_none()
    if device:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device asset number already exists.",
        )

    stmt = (
        select(tables.Brand)
        .where(tables.Brand.deleted_at.is_(None))
        .where(tables.Brand.id.__eq__(form_data.brand_id))
    )
    brand = db.scalars(stmt).one_or_none()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists.",
        )

    stmt = (
        select(tables.DeviceCategory)
        .where(tables.DeviceCategory.deleted_at.is_(None))
        .where(tables.DeviceCategory.id.__eq__(form_data.category_id))
    )
    device_category = db.scalars(stmt).one_or_none()
    if not device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device category not exists.",
        )
    form_data.creator_id = current_user.id
    device = tables.Device(**form_data.model_dump())
    db.add(device)
    db.commit()
    return device


# Update device.
@router.put("/{device_id}", response_model=schemas.Device)
async def update_device(
        db: databaseSession,
        device_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["device:update"]),
):
    stmt = (
        select(tables.Device)
        .where(tables.Device.deleted_at.is_(None))
        .where(tables.Device.id.__eq__(device_id))
    )
    device = db.scalars(stmt).one_or_none()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists.",
        )
    for form in form_data:
        if form.key == "brand_id":
            stmt = (
                select(tables.Brand)
                .where(tables.Brand.deleted_at.is_(None))
                .where(tables.Brand.id.__eq__(form.value))
            )
            brand = db.scalars(stmt).one_or_none()
            if not brand:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Brand not exists.",
                )
        elif form.key == "category_id":
            stmt = (
                select(tables.DeviceCategory)
                .where(tables.DeviceCategory.deleted_at.is_(None))
                .where(tables.DeviceCategory.id.__eq__(form.value))
            )
            device_category = db.scalars(stmt).one_or_none()
            if not device_category:
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
        setattr(device, form.key, form.value)
    db.commit()
    return device


# Delete device.
@router.delete("/{device_id}", response_model=schemas.Device)
async def delete_device(
        db: databaseSession,
        device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device:delete"]),
):
    stmt = (
        select(tables.Device)
        .where(tables.Device.deleted_at.is_(None))
        .where(tables.Device.id.__eq__(device_id))
    )
    device = db.scalars(stmt).one_or_none()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists.",
        )

    users = get_users(db, device)

    if users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device has users, please update them first.",
        )
    setattr(device, "deleted_at", common.now())
    db.commit()
    return device
