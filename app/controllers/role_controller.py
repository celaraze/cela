from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, crud, tables
from ..services.role import get_users

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
    roles = crud.select_all(db, tables.Role, skip=skip, limit=limit)
    return roles


@router.get("/trashed")
async def get_roles_trashed(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["role:list"]),
):
    roles = crud.select_all_with_trashed(db, tables.Role, skip=skip, limit=limit)
    return roles


@router.get("/{role_id}")
async def get_role(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:info"]),
):
    role = crud.select_id(db, tables.Role, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists",
        )
    return role


@router.get("/{role_id}/trashed")
async def get_role_trashed(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:info"]),
):
    role = crud.select_id(db, tables.Role, role_id, with_trashed=True)
    return role


@router.post("/")
async def create_role(
        db: databaseSession,
        form_data: schemas.RoleCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["role:create"]),
):
    db_role = crud.select_name(db, tables.Role, form_data.name)
    if db_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role already exists",
        )
    form_data.creator_id = current_user.id
    db_role = crud.create(db, tables.Role, form_data)
    return db_role


@router.put("/{role_id}")
async def update_role(
        db: databaseSession,
        role_id: int,
        form_data: schemas.UpdateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["role:update"]),
):
    db_role = crud.select_id(db, tables.Role, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists",
        )
    db_role = crud.update(db, tables.Role, db_role.id, form_data)
    return db_role


@router.delete("/{role_id}")
async def delete_role(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:delete"]),
):
    db_role = crud.select_id(db, tables.Role, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists",
        )
    users = get_users(db, role_id)
    if users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role has users, please update them first.",
        )
    db_role = crud.delete(db, tables.Role, role_id)
    return db_role


@router.put("/{role_id}/restore")
async def restore_role(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:restore"]),
):
    db_role = crud.select_id(db, tables.Role, role_id, with_trashed=True)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists",
        )
    db_role = crud.restore(db, tables.Role, role_id)
    return db_role


@router.delete("/{role_id}/force")
async def force_delete_role(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:force"]),
):
    db_role = crud.select_id(db, tables.Role, role_id, with_trashed=True)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists",
        )
    users = get_users(db, role_id)
    if users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role has users, please update them first.",
        )
    db_role = crud.force_delete(db, tables.Role, role_id)
    return db_role
