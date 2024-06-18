from fastapi import APIRouter, HTTPException, status, Security

from ..database import schemas, crud, tables
from ..dependencies import get_oauth_scheme, get_current_user, databaseSession

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/user_has_roles",
    tags=["user_has_roles"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_user_has_roles(
        db: databaseSession,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:list"]),
        skip: int = 0,
        limit: int = 100,
):
    user_has_roles = crud.select_all(db, tables.UserHasRole, skip=skip, limit=limit)
    if not user_has_roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User roles not exists",
        )
    return user_has_roles


@router.get("/trashed")
async def get_user_has_roles_trashed(
        db: databaseSession,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:list"]),
        skip: int = 0,
        limit: int = 100,
):
    user_has_roles = crud.select_all_with_trashed(db, tables.UserHasRole, skip=skip, limit=limit)
    if not user_has_roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User roles not exists",
        )
    return user_has_roles


@router.get("/{user_has_role_id}")
async def get_user_has_role(
        db: databaseSession,
        user_has_role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:info"]),
):
    user_has_role = crud.select_id(db, tables.UserHasRole, user_has_role_id)
    if not user_has_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists",
        )
    return user_has_role


@router.get("/{user_has_role_id}")
async def get_user_has_role_trashed(
        db: databaseSession,
        user_has_role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:info"]),
):
    user_has_role = crud.select_id(db, tables.UserHasRole, user_has_role_id, with_trashed=True)
    if not user_has_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists",
        )
    return user_has_role


@router.post("/")
async def create_user_has_role(
        db: databaseSession,
        form_data: schemas.UserHasRoleCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:create"]),
):
    db_user = crud.select_id(db, tables.User, form_data.user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    db_role = crud.select_id(db, tables.Role, form_data.role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists",
        )
    conditions = [
        schemas.QueryForm(key="user_id", operator="==", value=form_data.user_id),
        schemas.QueryForm(key="role_id", operator="==", value=form_data.role_id),
    ]
    db_user_has_roles = crud.selects(db, tables.UserHasRole, conditions)
    if db_user_has_roles:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User role already exists",
        )
    form_data.creator_id = current_user.id
    db_user_has_role = crud.create(db, tables.UserHasRole, form_data)
    return db_user_has_role


@router.delete("/{user_has_role_id}")
async def delete_user_has_role(
        db: databaseSession,
        user_has_role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:delete"]),
):
    db_user_has_role = crud.select_id(db, tables.UserHasRole, user_has_role_id)
    if not db_user_has_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists",
        )
    db_user_has_role = crud.delete(db, tables.UserHasRole, user_has_role_id)
    return db_user_has_role


@router.delete("/{user_id}/{role_id}")
async def delete_user_has_role_by_user_id_and_role_id(
        db: databaseSession,
        user_id: int,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:delete"]),
):
    conditions = [
        schemas.QueryForm(key="user_id", operator="==", value=user_id),
        schemas.QueryForm(key="role_id", operator="==", value=role_id),
    ]
    db_user_has_roles = crud.selects(db, tables.UserHasRole, conditions)
    if not db_user_has_roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists",
        )
    db_user_has_role = crud.delete_conditions(db, tables.UserHasRole, conditions)
    return db_user_has_role


@router.put("/{user_has_role_id}/restore")
async def restore_user_has_role(
        db: databaseSession,
        user_has_role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:restore"]),
):
    db_user_has_role = crud.select_id(db, tables.UserHasRole, user_has_role_id)
    if not db_user_has_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists",
        )
    db_user_has_role = crud.restore(db, tables.UserHasRole, user_has_role_id)
    return db_user_has_role


@router.delete("/{user_has_role_id}/force")
async def force_delete_user_has_role(
        db: databaseSession,
        user_has_role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:force_delete"]),
):
    db_user_has_role = crud.select_id(db, tables.UserHasRole, user_has_role_id, with_trashed=True)
    if not db_user_has_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists",
        )
    db_user_has_role = crud.force_delete(db, tables.UserHasRole, user_has_role_id)
    return db_user_has_role


@router.delete("/{user_id}/{role_id}/force")
async def force_delete_user_has_role_by_user_id_and_role_id(
        db: databaseSession,
        user_id: int,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:force_delete"]),
):
    conditions = [
        schemas.QueryForm(key="user_id", operator="==", value=user_id),
        schemas.QueryForm(key="role_id", operator="==", value=role_id),
    ]
    db_user_has_roles = crud.selects(db, tables.UserHasRole, conditions)
    if not db_user_has_roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists",
        )
    db_user_has_role = crud.force_delete_conditions(db, tables.UserHasRole, conditions)
    return db_user_has_role
