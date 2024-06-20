from fastapi import APIRouter, HTTPException, status, Security
from sqlalchemy import select

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..utils import common
from ..services.brand import get_devices

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/brands",
    tags=["brands"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# APIs for brand.


# Get all brands.
@router.get("/", response_model=list[schemas.Brand])
async def get_brands(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["brand:list"]),
):
    stmt = (
        select(tables.Brand)
        .where(tables.Brand.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    brands = db.scalars(stmt).all()
    return brands


# Get brand by id.
@router.get("/{brand_id}", response_model=schemas.Brand)
async def get_brand(
        db: databaseSession,
        brand_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["brand:info"]),
):
    stmt = (
        select(tables.Brand)
        .where(tables.Brand.deleted_at.is_(None))
        .where(tables.Brand.id.__eq__(brand_id))
    )
    brand = db.scalars(stmt).one_or_none()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists.",
        )
    return brand


# Create brand.
@router.post("/", response_model=schemas.Brand)
async def create_brand(
        db: databaseSession,
        form_data: schemas.BrandCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["brand:create"]),
):
    form_data.creator_id = current_user.id
    brand = tables.Brand(**form_data.dict())
    db.add(brand)
    db.commit()
    return brand


# Update brand.
@router.put("/{brand_id}", response_model=schemas.Brand)
async def update_brand(
        db: databaseSession,
        brand_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["brand:update"]),
):
    stmt = (
        select(tables.Brand)
        .where(tables.Brand.deleted_at.is_(None))
        .where(tables.Brand.id.__eq__(brand_id))
    )
    brand = db.scalars(stmt).one_or_none()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists.",
        )
    for form in form_data:
        setattr(brand, form.key, form.value)
    db.commit()
    return brand


# Delete brand.
@router.delete("/{brand_id}", response_model=schemas.Brand)
async def delete_brand(
        db: databaseSession,
        brand_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["brand:delete"]),
):
    stmt = (
        select(tables.Brand)
        .where(tables.Brand.deleted_at.is_(None))
        .where(tables.Brand.id.__eq__(brand_id))
    )
    brand = db.scalars(stmt).one_or_none()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists.",
        )

    devices = get_devices(brand)

    if devices:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Brand has devices, please update devices first.",
        )
    setattr(brand, "deleted_at", common.now())
    db.commit()
    return brand
