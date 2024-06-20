from fastapi import APIRouter, HTTPException, status, Security
from sqlalchemy import select

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..utils import common
from ..services.device_category import get_devices

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/device_categories",
    tags=["device_categories"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# APIs for device category.

# Get all device categories.
@router.get("/", response_model=list[schemas.DeviceCategory])
async def get_device_categories(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:list"]),
):
    stmt = (
        select(tables.DeviceCategory)
        .where(tables.DeviceCategory.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    device_categories = db.scalars(stmt).all()
    return device_categories


# Get device category by id.
@router.get("/{device_category_id}", response_model=schemas.DeviceCategory)
async def get_device_category(
        db: databaseSession,
        device_category_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:info"]),
):
    stmt = (
        select(tables.DeviceCategory)
        .where(tables.DeviceCategory.deleted_at.is_(None))
        .where(tables.DeviceCategory.id.__eq__(device_category_id))
    )
    device_category = db.scalars(stmt).one_or_none()
    if not device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Category not exists.",
        )
    return device_category


# Create device category.
@router.post("/", response_model=schemas.DeviceCategory)
async def create_device_category(
        db: databaseSession,
        form_data: schemas.DeviceCategoryCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:create"]),
):
    form_data.creator_id = current_user.id
    device_category = tables.DeviceCategory(**form_data.dict())
    db.add(device_category)
    db.commit()
    return device_category


# Update device category.
@router.put("/{device_category_id}", response_model=schemas.DeviceCategory)
async def update_device_category(
        db: databaseSession,
        device_category_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:update"]),
):
    stmt = (
        select(tables.DeviceCategory)
        .where(tables.DeviceCategory.deleted_at.is_(None))
        .where(tables.DeviceCategory.id.__eq__(device_category_id))
    )
    device_category = db.scalars(stmt).one_or_none()
    if not device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Category not exists.",
        )
    for form in form_data:
        setattr(device_category, form.key, form.value)
    db.commit()
    return device_category


# Delete device category.
@router.delete("/{device_category_id}", response_model=schemas.DeviceCategory)
async def delete_device_category(
        db: databaseSession,
        device_category_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:delete"]),
):
    stmt = (
        select(tables.DeviceCategory)
        .where(tables.DeviceCategory.deleted_at.is_(None))
        .where(tables.DeviceCategory.id.__eq__(device_category_id))
    )
    device_category = db.scalars(stmt).one_or_none()
    if not device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Category not exists.",
        )

    devices = get_devices(device_category)

    if devices:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device Category has devices, please update them first.",
        )
    setattr(device_category, "deleted_at", common.now())
    db.commit()
    return device_category
