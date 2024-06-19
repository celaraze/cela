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


# APIs for role.


# Get all roles.
@router.get("/", response_model=list[schemas.Role])
async def get_roles(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["role:list"]),
):
    roles = crud.select_all(db, tables.Role, skip=skip, limit=limit)
    return roles


# Get role by id.
@router.get("/{role_id}", response_model=schemas.Role)
async def get_role(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:info"]),
):
    role = crud.select_id(db, tables.Role, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists.",
        )
    role.creator = crud.select_creator(db, tables.User, role.creator_id)
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
    db_role = crud.create(db, tables.Role, form_data)
    return db_role


# Update role.
@router.put("/{role_id}", response_model=schemas.Role)
async def update_role(
        db: databaseSession,
        role_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["role:update"]),
):
    db_role = crud.select_id(db, tables.Role, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists.",
        )
    if db_role.name == "superuser":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role name 'superuser' is reserved.",
        )
    db_role = crud.update(db, tables.Role, db_role.id, form_data)
    return db_role


# Delete role.
@router.delete("/{role_id}", response_model=schemas.Role)
async def delete_role(
        db: databaseSession,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["role:delete"]),
):
    db_role = crud.select_id(db, tables.Role, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists.",
        )
    if db_role.name == "superuser":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role name 'superuser' is reserved.",
        )
    users = get_users(db, role_id)
    if users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role has users, please update them first.",
        )
    db_role = crud.delete(db, tables.Role, role_id)
    return db_role
