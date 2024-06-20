from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..services.brand import get_devices
from ..utils import common

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
    brands = (
        db.query(tables.Brand)
        .filter(tables.Brand.deleted_at.isnot(None))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return brands


# Get brand by id.
@router.get("/{brand_id}", response_model=schemas.Brand)
async def get_brand(
        db: databaseSession,
        brand_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["brand:info"]),
):
    brand = (
        db.query(tables.Brand)
        .filter(tables.Brand.deleted_at.isnot(None))
        .filter(tables.Brand.id == brand_id)
        .first()
    )
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists.",
        )
    brand.creator = (
        db.query(tables.User)
        .filter(tables.User.deleted_at.isnot(None))
        .filter(tables.User.id == brand.creator_id)
        .first()
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
    db.refresh(brand)
    return brand


# Update brand.
@router.put("/{brand_id}", response_model=schemas.Brand)
async def update_brand(
        db: databaseSession,
        brand_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["brand:update"]),
):
    db_brand = (
        db.query(tables.Brand)
        .filter(tables.Brand.deleted_at.isnot(None))
        .filter(tables.Brand.id == brand_id)
        .first()
    )
    if not db_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists.",
        )
    for form in form_data:
        setattr(db_brand, form.key, form.value)
    db.commit()
    db.refresh(db_brand)
    return db_brand


# Delete brand.
@router.delete("/{brand_id}", response_model=schemas.Brand)
async def delete_brand(
        db: databaseSession,
        brand_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["brand:delete"]),
):
    db_brand = (
        db.query(tables.Brand)
        .filter(tables.Brand.deleted_at.isnot(None))
        .filter(tables.Brand.id == brand_id)
        .first()
    )
    if not db_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not exists.",
        )
    devices = get_devices(db, brand_id)
    if devices:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Brand has devices, please update devices first.",
        )
    setattr(db_brand, "deleted_at", common.now())
    db.commit()
    db.refresh(db_brand)
    return db_brand
