from fastapi import APIRouter, HTTPException, status, Security
from sqlalchemy import select

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..utils import common

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# APIs for role.


# Get all roles.
@router.get("/", response_model=list[schemas.Role])
async def get_roles(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["role:list"]),
):
    stmt = (
        select(tables.Role)
        .where(tables.Role.deleted_at.isnot(None))
        .offset(skip)
        .limit(limit)
    )
    roles = db.scalars(stmt).all()
    return roles


# Get role by id.
@router.get("/{role_id}", response_model=schemas.Role)
async def get_role(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:info"]),
):
    stmt = (
        select(tables.Role)
        .where(tables.Role.deleted_at.isnot(None))
        .where(tables.Role.id.__eq__(role_id))
    )
    role = db.scalars(stmt).one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists.",
        )
    return role


# Create role.
@router.post("/", response_model=schemas.Role)
async def create_role(
        db: databaseSession,
        form_data: schemas.RoleCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["role:create"]),
):
    if form_data.name == "superuser":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role name 'superuser' is reserved.",
        )
    form_data.creator_id = current_user.id
    role = tables.Role(**form_data.dict())
    db.add(role)
    return role


# Update role.
@router.put("/{role_id}", response_model=schemas.Role)
async def update_role(
        db: databaseSession,
        role_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["role:update"]),
):
    stmt = (
        select(tables.Role)
        .where(tables.Role.deleted_at.isnot(None))
        .where(tables.Role.id.__eq__(role_id))
    )
    role = db.scalars(stmt).one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists.",
        )
    if role.name == "superuser":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role name 'superuser' is reserved.",
        )
    for form in form_data:
        setattr(role, form.key, form.value)
    db.commit()
    return role


# Delete role.
@router.delete("/{role_id}", response_model=schemas.Role)
async def delete_role(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:delete"]),
):
    stmt = (
        select(tables.Role)
        .where(tables.Role.deleted_at.isnot(None))
        .where(tables.Role.id.__eq__(role_id))
    )
    role = db.scalars(stmt).one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists.",
        )
    if role.name == "superuser":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role name 'superuser' is reserved.",
        )
    if role.users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role has users, please update them first.",
        )
    setattr(role, "deleted_at", common.now())
    return role
