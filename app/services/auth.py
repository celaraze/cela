from datetime import timedelta, datetime, timezone
from typing import Union

from jose import jwt
from sqlalchemy import select

from ..database import schemas, tables
from ..utils import crypt
from ..utils.config import get_jwt_config


def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=get_jwt_config()['ttl_minutes'])
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_jwt_config()['secret'], algorithm=get_jwt_config()['algorithm'])
    return encoded_jwt


def decode_access_token(token: str):
    payload = jwt.decode(token, get_jwt_config()['secret'], algorithms=[get_jwt_config()['algorithm']])
    return payload


def authenticate(
        db,
        username: str,
        password: str,
) -> Union[schemas.User, bool]:
    stmt = (
        select(tables.User)
        .where(tables.User.deleted_at.is_(None))
        .where(tables.User.username.__eq__(username))
    )
    user = db.scalars(stmt).one_or_none()
    if not user:
        return False
    if not crypt.verify_hashed_password(password, user.hashed_password):
        return False
    return user


def create_super_admin(db, form_data: schemas.UserCreateForm):
    try:
        stmt = (
            select(tables.Role)
            .where(tables.Role.name.__eq__("superuser"))
        )
        role = db.scalars(stmt).one_or_none()
        if not role:
            print("Creating a superuser role.")
            role_create = schemas.RoleCreateForm(
                name="superuser",
                scopes=["su"]
            )
            role = tables.Role(**role_create.dict())
            db.add(role)
            db.commit()
            print("Superuser role created successfully.")
        else:
            print("Superuser role already exists.")

        stmt = (
            select(tables.User)
            .where(tables.User.username.__eq__(form_data.username))
        )
        user = db.scalars(stmt).one_or_none()
        if not user:
            form_data.hashed_password = crypt.hash_password(form_data.password)
            del form_data.password
            form_data.creator_id = form_data.creator_id
            user = tables.User(**form_data.dict())
            db.add(user)
            db.commit()
        else:
            print("User already exists.")
        if role in user.roles:
            print("User already has superuser role.")
        else:
            user.roles.append(role)
            db.commit()
            print("Superuser role added to user.")

        print("Super admin created successfully.")
        return user
    except Exception as e:
        print("Error creating super admin.")
        raise e
