from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..services.device_category import get_devices
from ..utils import common

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
    device_categories = (
        db.query(tables.DeviceCategory)
        .filter(tables.DeviceCategory.deleted_at.isnot(None))
        .offset(skip).limit(limit)
        .all()
    )
    return device_categories


# Get device category by id.
@router.get("/{device_category_id}", response_model=schemas.DeviceCategory)
async def get_device_category(
        db: databaseSession,
        device_category_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:info"]),
):
    device_category = (
        db.query(tables.DeviceCategory)
        .filter(tables.DeviceCategory.deleted_at.isnot(None))
        .filter(tables.DeviceCategory.id == device_category_id)
        .first()
    )
    if not device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Category not exists.",
        )
    device_category.creator = (
        db.query(tables.User)
        .filter(tables.User.id == device_category.creator_id)
        .first()
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
    db.refresh(device_category)
    return device_category


# Update device category.
@router.put("/{device_category_id}", response_model=schemas.DeviceCategory)
async def update_device_category(
        db: databaseSession,
        device_category_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:update"]),
):
    db_device_category = (
        db.query(tables.DeviceCategory)
        .filter(tables.DeviceCategory.deleted_at.isnot(None))
        .filter(tables.DeviceCategory.id == device_category_id)
        .first()
    )
    if not db_device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Category not exists.",
        )
    for form in form_data:
        setattr(db_device_category, form.key, form.value)
    db.commit()
    db.refresh(db_device_category)
    return db_device_category


# Delete device category.
@router.delete("/{device_category_id}", response_model=schemas.DeviceCategory)
async def delete_device_category(
        db: databaseSession,
        device_category_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:delete"]),
):
    db_device_category = (
        db.query(tables.DeviceCategory)
        .filter(tables.DeviceCategory.deleted_at.isnot(None))
        .filter(tables.DeviceCategory.id == device_category_id)
        .first()
    )
    if not db_device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Category not exists.",
        )
    devices = get_devices(db, device_category_id)
    if devices:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device Category has devices, please update them first.",
        )
    setattr(db_device_category, "deleted_at", common.now())
    db.commit()
    db.refresh(db_device_category)
    return db_device_category
