from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas
from ..models.role import Role

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_roles(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["role:list"]),
):
    roles = Role.select_all(db, skip=skip, limit=limit)
    return roles


@router.get("/{role_id}")
async def get_role(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:info"]),
):
    role = Role.select_one(db, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists",
        )
    return role


@router.post("/")
async def create_role(
        db: databaseSession,
        form_data: schemas.RoleCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["role:create"]),
):
    db_role = Role.select_one_by_name(db, form_data.name)
    if db_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role already exists",
        )
    form_data.creator_id = current_user.id
    db_role = Role.create(db, form_data)
    return db_role


@router.put("/{role_id}")
async def update_role(
        db: databaseSession,
        role_id: int,
        form_data: schemas.UpdateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["role:update"]),
):
    db_role = Role.select_one(db, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists",
        )
    db_role = Role.update(db, db_role.id, form_data)
    return db_role


@router.delete("/{role_id}")
async def delete_role(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:delete"]),
):
    db_role = Role.select_one(db, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists",
        )
    db_role = Role.delete(db, role_id)
    return db_role
