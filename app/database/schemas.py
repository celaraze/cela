from datetime import datetime
from typing import Union

from pydantic import BaseModel as BaseSchema


# schema for decoding token
class AuthTokenData(BaseSchema):
    username: str
    scopes: list[str] = []


# Form schemas #
class UpdateForm(BaseSchema):
    key: str
    value: Union[str, list[str]]


class RoleCreateForm(BaseSchema):
    name: str
    scopes: list[str] = []


class UserChangePasswordForm(BaseSchema):
    old_password: str
    new_password: str


class UserCreateForm(BaseSchema):
    username: str
    email: str
    name: str
    password: str
    creator_id: Union[int, None] = None


class BrandCreateForm(BaseSchema):
    name: str
    creator_id: Union[int, None] = None


class DeviceCategoryCreateForm(BaseSchema):
    name: str
    creator_id: Union[int, None] = None


class UserHasRoleCreateForm(BaseSchema):
    user_id: int
    role_id: int


# Model schemas #
class Role(BaseSchema):
    id: int
    name: str
    scopes: list[str]
    created_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None

    class Config:
        from_attributes = True


class User(BaseSchema):
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


class Footprint(BaseSchema):
    id: int
    url: str
    action: str
    request_body: dict
    response_status_code: int
    response_body: dict
    user_id: int
    created_at: datetime
    creator: Union[User, None] = None


class UserHasRole(BaseSchema):
    id: int
    user_id: int
    role_id: int
    created_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None

    class Config:
        from_attributes = True


class UserHasDevice(BaseSchema):
    id: int
    user_id: int
    device_id: int
    flag: int
    message: Union[str, None] = None
    expired_at: Union[datetime, None] = None
    created_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None

    class Config:
        from_attributes = True


class Brand(BaseSchema):
    id: int
    name: str
    creator_id: Union[int, None] = None
    created_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None
    creator: Union[User, None] = None


class DeviceCategory(BaseSchema):
    id: int
    name: str
    creator_id: Union[int, None] = None
    created_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None
    creator: Union[User, None] = None


class Device(BaseSchema):
    id: int
    hostname: str
    asset_number: str
    ipv4_address: Union[str, None] = None
    ipv6_address: Union[str, None] = None
    mac_address: Union[str, None] = None
    description: Union[str, None] = None
    brand: Brand
    category: DeviceCategory
    created_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None
    creator: Union[User, None] = None
