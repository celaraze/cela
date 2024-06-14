from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import get_current_user, databaseSession
from ..services.auth import authenticate, create_access_token
from ..database import schemas
from ..models.user import User
from ..utils import crypt

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
async def login(
        db: databaseSession,
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    scopes = User.get_scopes(db, user.id)
    access_token = create_access_token(data={"user_id": user.id, "scopes": scopes})
    return {"access_token": access_token, "type": "bearer"}


@router.get("/me")
async def me(
        current_user: schemas.User = Security(get_current_user, scopes=["auth:me"]),
):
    return current_user


@router.put("/me")
async def update_me(
        db: databaseSession,
        form_data: schemas.UpdateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["auth:me"]),
):
    current_user = User.update(db, current_user.id, form_data)
    return current_user


@router.put("/change_password")
async def change_password(
        db: databaseSession,
        form_data: schemas.UserChangePasswordForm,
        current_user: schemas.User = Security(get_current_user, scopes=["auth:me"]),
):
    user = authenticate(db, current_user.username, form_data.old_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    update_form = schemas.UpdateForm(key="hashed_password", value=crypt.hash_password(form_data.new_password))
    current_user = User.update(db, current_user.id, update_form)
    return current_user


@router.post("/renew")
async def refresh_scopes(
        db: databaseSession,
        current_user: schemas.User = Security(get_current_user, scopes=["auth:me"]),
):
    scopes = User.get_scopes(db, current_user.id)
    access_token = create_access_token(data={"user_id": current_user.id, "scopes": scopes})
    return {"access_token": access_token, "type": "bearer"}
