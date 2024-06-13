from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_oauth_scheme, get_current_user
from ..services import auth
from ..services.auth import authenticate, create_access_token
from ..database import schemas
from ..models.user import User
from ..utils import crypt

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    user = authenticate(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    scopes = auth.get_scopes(user)
    access_token = create_access_token(data={"username": user.username, "scopes": scopes})
    return {"access_token": access_token, "type": "bearer"}


@router.get("/me")
async def me(
        current_user: schemas.User = Security(get_current_user, scopes=["auth:me"]),
):
    return current_user


@router.put("/me")
async def update_me(
        form_data: schemas.UpdateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["auth:me"]),
        db: Session = Depends(get_db),
):
    current_user = User.update(db, current_user, form_data)
    return current_user


@router.put("/change_password")
async def change_password(
        form_data: schemas.AuthChangePassword,
        current_user: schemas.User = Security(get_current_user, scopes=["auth:me"]),
        db: Session = Depends(get_db),
):
    user = authenticate(current_user.username, form_data.old_password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    update = schemas.UpdateForm(key="hashed_password", value=crypt.hash_password(form_data.new_password))
    current_user = User.update(db, current_user, update)
    return current_user


@router.post("/renew")
async def refresh_scopes(
        current_user: schemas.User = Security(get_current_user, scopes=["auth:me"]),
):
    scopes = auth.get_scopes(current_user)
    access_token = create_access_token(data={"username": current_user.username, "scopes": scopes})
    return {"access_token": access_token, "type": "bearer"}
