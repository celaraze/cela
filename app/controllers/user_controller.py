from fastapi import APIRouter, HTTPException, status, Security

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, crud, tables
from ..utils import crypt

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_users(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["user:list"]),
):
    users = crud.select_all(db, tables.User, skip=skip, limit=limit)
    return users


@router.get("/{user_id}")
async def get_user(
        db: databaseSession,
        user_id: int = None,
        include_deleted: bool = False,
        current_user: schemas.User = Security(get_current_user, scopes=["user:info"]),
):
    user = crud.select_id(db, tables.User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    if not include_deleted:
        if user.deleted_at:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not exists",
            )
    return user


@router.post("/", response_model=schemas.User)
async def create_user(
        db: databaseSession,
        form_data: schemas.UserCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user:create"]),
):
    db_user = crud.select_email(db, tables.User, form_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )
    db_user = crud.select_username(db, tables.User, form_data.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    form_data.creator_id = current_user.id
    db_user = crud.create_user(db, tables.User, form_data)
    return db_user


@router.put("/{user_id}")
async def update_user(
        db: databaseSession,
        user_id: int,
        form_data: schemas.UpdateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["user:update"]),
):
    db_user = crud.select_id(db, tables.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    if form_data.key not in ["username", "name", "email", "password"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ony username, name, email and password can be updated",
        )
    if form_data.key == "password":
        form_data.key = "hashed_password"
        form_data.value = crypt.hash_password(form_data.value)
    db_user = crud.update(db, tables.User, db_user.id, form_data)
    return db_user


@router.delete("/{user_id}")
async def delete_user(
        db: databaseSession,
        user_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["user:delete"]),
):
    db_user = crud.select_id(db, tables.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists",
        )
    db_user = crud.delete(db, tables.User, user_id)
    return db_user
