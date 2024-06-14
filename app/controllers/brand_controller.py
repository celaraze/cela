from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user
from ..database import schemas
from ..models.brand import Brand

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/brands",
    tags=["brands"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_brands(
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["role:list"]),
):
    brands = Brand.select_all(skip=skip, limit=limit)
    return brands


@router.get("/{brand_id}")
async def get_brand(
        brand_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:info"]),
):
    brand = Brand.select_one(brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists",
        )
    return brand


@router.post("/")
async def create_brand(
        form_data: schemas.BrandCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["role:create"]),
):
    db_brand = Brand.select_one_by_name(form_data.name)
    if db_brand:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Brand already exists",
        )
    form_data.creator_id = current_user.id
    db_role = Brand.create(form_data)
    return db_role


@router.put("/{brand_id}")
async def update_brand(
        brand_id: int,
        form_data: schemas.UpdateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["role:update"]),
):
    db_brand = Brand.select_one(brand_id)
    if not db_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists",
        )
    db_brand = Brand.update(brand_id, form_data)
    return db_brand


@router.delete("/{brand_id}")
async def delete_brand(
        brand_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:delete"]),
):
    db_brand = Brand.select_one(brand_id)
    if not db_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists",
        )
    db_brand = Brand.delete(brand_id)
    return db_brand
