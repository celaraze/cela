from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, crud, tables
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
    device_categories = crud.select_all(db, tables.DeviceCategory, skip=skip, limit=limit)
    return device_categories


# Get device category by id.
@router.get("/{device_category_id}", response_model=schemas.DeviceCategory)
async def get_device_category(
        db: databaseSession,
        device_category_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:info"]),
):
    device_category = crud.select_id(db, tables.DeviceCategory, device_category_id)
    if not device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Category not exists.",
        )
    device_category.creator = crud.select_creator(db, tables.User, device_category.creator_id)
    return device_category


# Create device category.
@router.post("/", response_model=schemas.DeviceCategory)
async def create_device_category(
        db: databaseSession,
        form_data: schemas.DeviceCategoryCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:create"]),
):
    form_data.creator_id = current_user.id
    db_device_category = crud.create(db, tables.DeviceCategory, form_data)
    return db_device_category


# Update device category.
@router.put("/{device_category_id}", response_model=schemas.DeviceCategory)
async def update_device_category(
        db: databaseSession,
        device_category_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:update"]),
):
    db_device_category = crud.select_id(db, tables.DeviceCategory, device_category_id)
    if not db_device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Category not exists.",
        )
    db_device_category = crud.update(db, tables.DeviceCategory, device_category_id, form_data)
    return db_device_category


# Delete device category.
@router.delete("/{device_category_id}", response_model=schemas.DeviceCategory)
async def delete_device_category(
        db: databaseSession,
        device_category_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["device_category:delete"]),
):
    db_device_category = crud.select_id(db, tables.DeviceCategory, device_category_id)
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
    db_device_category = crud.delete(db, tables.DeviceCategory, device_category_id)
    return db_device_category
