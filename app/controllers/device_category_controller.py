from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user
from ..database import schemas
from ..models.device_category import DeviceCategory

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/device_categories",
    tags=["device_categories"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_device_categories(
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["role:list"]),
):
    device_categories = DeviceCategory.select_all(skip=skip, limit=limit)
    return device_categories


@router.get("/{device_category_id}")
async def get_device_category(
        brand_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:info"]),
):
    device_category = DeviceCategory.select_one(brand_id)
    if not device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Category not exists",
        )
    return device_category


@router.post("/")
async def create_device_category(
        form_data: schemas.DeviceCategoryCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["role:create"]),
):
    db_device_category = DeviceCategory.select_one_by_name(form_data.name)
    if db_device_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device Category already exists",
        )
    form_data.creator_id = current_user.id
    db_device_category = DeviceCategory.create(form_data)
    return db_device_category


@router.put("/{device_category_id}")
async def update_device_category(
        device_category_id: int,
        form_data: schemas.UpdateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["role:update"]),
):
    db_device_category = DeviceCategory.select_one(device_category_id)
    if not db_device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Category not exists",
        )
    db_device_category = DeviceCategory.update(device_category_id, form_data)
    return db_device_category


@router.delete("/{device_category_id}")
async def delete_device_category(
        device_category_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:delete"]),
):
    db_device_category = DeviceCategory.select_one(device_category_id)
    if not db_device_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Category not exists",
        )
    db_device_category = DeviceCategory.delete(device_category_id)
    return db_device_category
