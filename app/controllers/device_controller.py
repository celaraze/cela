from fastapi import APIRouter, HTTPException, status, Security
from sqlalchemy import select

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..utils import common
from ..services.device import get_brand, get_category, get_user, get_historical_users

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
    device.users = get_user(db, device)
    return device


# Create device.
@router.post("/", response_model=schemas.Device)
async def create_device(
        db: databaseSession,
        form_data: schemas.DeviceCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["device:create"]),
):
    stmt = (
        select(tables.Device)
        .where(tables.Device.deleted_at.is_(None))
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

    if common.check_asset_number(db, form_data.asset_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Asset number already exists.",
        )

    form_data.creator_id = current_user.id
    device = tables.Device(**form_data.model_dump())
    db.add(device)
    db.commit()

    asset_number_form = schemas.AssetNumberCreateForm(
        number=form_data.asset_number,
        table_name="Device",
        table_id=device.id,
        creator_id=current_user.id,
    )

    asset_number = tables.AssetNumber(**asset_number_form.model_dump())
    db.add(asset_number)

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

    users = get_user(db, device)

    if users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device has users, please update them first.",
        )
    setattr(device, "deleted_at", common.now())

    stmt = (
        select(tables.AssetNumber)
        .where(tables.AssetNumber.deleted_at.is_(None))
        .where(tables.AssetNumber.table_name.__eq__("Device"))
        .where(tables.AssetNumber.table_id.__eq__(device_id))
    )
    asset_number = db.scalars(stmt).one_or_none()
    if asset_number:
        setattr(asset_number, "deleted_at", common.now())
    db.commit()
    return device


# API for user has device.

# Get device users.
@router.get("/{device_id}/users", response_model=list[schemas.UserForDevice])
async def get_device_users(
        db: databaseSession,
        device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device:users"]),
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

    users = get_historical_users(db, device)
    return users


# Get historical users.
@router.get("/{device_id}/users/historical", response_model=list[schemas.DeviceHistoricalUser])
async def select_role_historical_users(
        db: databaseSession,
        device_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:historical"]),
):
    stmt = (
        select(tables.Device)
        .where(tables.Device.id.__eq__(device_id))
    )
    device = db.scalars(stmt).one_or_none()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exists.",
        )
    historical_users = get_historical_users(db, device)
    return historical_users
