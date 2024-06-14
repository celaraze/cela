from fastapi import APIRouter, HTTPException, status, Security

from ..database import schemas
from ..dependencies import get_oauth_scheme, get_current_user
from ..models.role import Role
from ..models.user import User
from ..models.user_has_role import UserHasRole

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/user_has_roles",
    tags=["user_has_roles"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_user_has_roles(
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:list"]),
        skip: int = 0,
        limit: int = 100,
):
    user_has_roles = UserHasRole.select_all(skip=skip, limit=limit)
    if not user_has_roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User roles not exists",
        )
    return user_has_roles


@router.get("/{user_has_role_id}")
async def get_user_has_role(
        user_has_role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:info"]),
):
    user_has_role = UserHasRole.select_one(user_has_role_id)
    if not user_has_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists",
        )
    return user_has_role


@router.post("/")
async def create_user_has_role(
        form_data: schemas.UserHasRoleCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:create"]),
):
    db_user = User.select_one(form_data.user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    db_role = Role.select_one(form_data.role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not exists",
        )
    form_data.creator_id = current_user.id
    db_user_has_role = UserHasRole.create(form_data)
    return db_user_has_role


@router.delete("/{user_has_role_id}")
async def delete_user_has_role(
        user_has_role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:delete"]),
):
    db_user_has_role = UserHasRole.select_one(user_has_role_id)
    if not db_user_has_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists",
        )
    db_user_has_role = UserHasRole.delete(user_has_role_id)
    return db_user_has_role


@router.delete("/{user_id}/{role_id}")
async def delete_user_has_role_by_user_id_and_role_id(
        user_id: int,
        role_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user_has_role:delete"]),
):
    db_user_has_role = UserHasRole.select_one_by_user_id_and_role_id(user_id, role_id)
    if not db_user_has_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not exists",
        )
    db_user_has_role = UserHasRole.delete_by_user_id_and_role_id(user_id, role_id)
    return db_user_has_role
