from fastapi import APIRouter, HTTPException, status, Security
from sqlalchemy import select

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..utils import common
from ..services.role import get_users, get_historical_users

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
async def select_roles(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["role:list"]),
):
    stmt = (
        select(tables.Role)
        .where(tables.Role.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    roles = db.scalars(stmt).all()
    return roles


# Get role by id.
@router.get("/{role_id}", response_model=schemas.Role)
async def select_role(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:info"]),
):
    stmt = (
        select(tables.Role)
        .where(tables.Role.deleted_at.is_(None))
        .where(tables.Role.id.__eq__(role_id))
    )
    role = db.scalars(stmt).one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists.",
        )
    role.creator = common.get_creator(db, role.creator_id)
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
    role = tables.Role(**form_data.model_dump())
    db.add(role)
    db.commit()
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
        .where(tables.Role.deleted_at.is_(None))
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
        .where(tables.Role.deleted_at.is_(None))
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

    users = get_users(db, role)

    if users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role has users, please update them first.",
        )
    setattr(role, "deleted_at", common.now())
    db.commit()
    return role


# API for user has role.
# Get role users.
@router.get("/{role_id}/users", response_model=list[schemas.UserForRole])
async def select_role_users(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:list"]),
):
    stmt = (
        select(tables.Role)
        .where(tables.Role.deleted_at.is_(None))
        .where(tables.Role.id.__eq__(user_id))
    )
    role = db.scalars(stmt).one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists.",
        )
    users = get_users(db, role)
    return users


# Get historical users.
@router.get("/{role_id}/users/historical", response_model=list[schemas.RoleHistoricalUser])
async def select_role_historical_users(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:historical"]),
):
    stmt = (
        select(tables.Role)
        .where(tables.Role.id.__eq__(role_id))
    )
    role = db.scalars(stmt).one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists.",
        )
    historical_users = get_historical_users(db, role)
    return historical_users
