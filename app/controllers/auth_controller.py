from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from ..dependencies import get_current_user, databaseSession
from ..services.auth import authenticate, create_access_token, create_super_admin
from ..services.user import get_roles
from ..database import schemas, tables
from ..utils import crypt

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/init")
async def init(
        db: databaseSession,
):
    admin = db.query(tables.User).filter(tables.User.username == "admin").first()
    if admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cela has been inited.",
        )
    username = "admin"
    email = "admin@localhost"
    name = "Admin"
    password = "admin"
    create_super_admin(
        db,
        schemas.UserCreateForm(
            username=username,
            email=email,
            name=name,
            password=password,
        )
    )
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Cela inited successfully, please login with username 'admin' and password 'admin' by default.",
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
    scopes = []
    roles = get_roles(db, user)
    for role in roles:
        scopes.extend(role.scopes)
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
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["auth:me"]),
):
    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.is_(None))
        .where(tables.User.id.__eq__(current_user.id))
    )
    user = db.execute(stmt).scalar_one()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists.",
        )
    for form in form_data:
        setattr(user, form.key, form.value)
    db.commit()
    return user


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
    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.is_(None))
        .where(tables.User.id.__eq__(current_user.id))
    )
    user = db.execute(stmt).scalar_one()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not exists.",
        )
    setattr(user, "hashed_password", crypt.hash_password(form_data.new_password))
    db.commit()
    return user


@router.post("/renew")
async def refresh_scopes(
        db: databaseSession,
        current_user: schemas.User = Security(get_current_user, scopes=["auth:me"]),
):
    scopes = []
    roles = get_roles(db, current_user)
    for role in roles:
        scopes.extend(role.scopes)
    access_token = create_access_token(data={"user_id": current_user.id, "scopes": scopes})
    return {"access_token": access_token, "type": "bearer"}
