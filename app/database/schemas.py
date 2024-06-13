from datetime import datetime
from typing import Union

from pydantic import BaseModel


class UpdateForm(BaseModel):
    key: str
    value: Union[str, list[str]]


# schema for returning token
class AuthToken(BaseModel):
    type: str
    access_token: str


# schema for decoding token
class AuthTokenData(BaseModel):
    username: str
    scopes: list[str] = []


class AuthChangePassword(BaseModel):
    old_password: str
    new_password: str


class Role(BaseModel):
    id: int
    name: str
    scopes: list[str]

    class Config:
        from_attributes = True


class RoleForm(BaseModel):
    name: str
    scopes: list[str] = []


# Base schema for user
class User(BaseModel):
    id: int
    username: str
    email: str
    name: str
    is_active: bool = True
    creator_id: Union[int, None] = None
    created_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None
    roles: list[Role] = []
    scopes: list[str] = []

    class Config:
        from_attributes = True


# schema for creating user
class UserForm(BaseModel):
    username: str
    email: str
    name: str
    password: str
    creator_id: Union[int, None] = None


class UserHasRole(BaseModel):
    id: int
    user_id: int
    role_id: int

    class Config:
        from_attributes = True


class UserHasRoleForm(BaseModel):
    user_id: int
    role_id: int
