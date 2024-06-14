from datetime import timedelta, datetime, timezone
from typing import Union

from jose import jwt

from ..models.user import User
from ..models.role import Role
from ..models.user_has_role import UserHasRole
from ..database import schemas
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
    user = User.select_one_by_username(db, username)
    if not user:
        return False
    if not crypt.verify_hashed_password(password, user.hashed_password):
        return False
    return user


def create_super_admin(db, form_data: schemas.UserCreateForm):
    try:
        role = Role.select_one_by_name(db, "superuser")
        if not role:
            print("Creating a superuser role.")
            role_create = schemas.RoleCreateForm(
                name="superuser",
                scopes=["su"]
            )
            role = Role.create(db, role_create)
            print("Superuser role created successfully.")
        else:
            print("Superuser role already exists.")
        user = User.create(db, form_data)
        if not user:
            print("Error creating super user.")
            return

        user_has_role = schemas.UserHasRoleCreateForm(
            user_id=user.id,
            role_id=role.id,
        )
        user_has_role = UserHasRole.create(db, user_has_role)
        if user_has_role:
            print("User has superuser role.")

        print("Super admin created successfully.")
    except Exception as e:
        print("Error creating super admin.")
        print(e)
