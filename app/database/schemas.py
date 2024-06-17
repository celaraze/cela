from datetime import datetime
from typing import Union, Any

from pydantic import BaseModel as BaseSchema

from app.utils import common


# schema for decoding token
class AuthTokenData(BaseSchema):
    user_id: int
    scopes: list[str] = []


# form schemas #
class UpdateForm(BaseSchema):
    key: str
    value: Union[str, list[str]]


class QueryForm(BaseSchema):
    key: str
    value: Any


class RoleCreateForm(BaseSchema):
    name: str
    scopes: list[str] = []
    creator_id: int = 0
    created_at: datetime = common.now()


class UserChangePasswordForm(BaseSchema):
    old_password: str
    new_password: str


class UserCreateForm(BaseSchema):
    username: str
    email: str
    name: str
    password: str
    creator_id: int = 0
    created_at: datetime = common.now()


class BrandCreateForm(BaseSchema):
    name: str
    creator_id: int = 0
    created_at: datetime = common.now()


class DeviceCategoryCreateForm(BaseSchema):
    name: str
    creator_id: int = 0
    created_at: datetime = common.now()


class UserHasRoleCreateForm(BaseSchema):
    user_id: int
    role_id: int
    creator_id: int = 0
    created_at: datetime = common.now()


class UserHasDeviceCreateForm(BaseSchema):
    user_id: int
    device_id: int
    flag: int
    message: Union[str, None] = None
    expired_at: Union[datetime, None] = None
    returned_at: Union[datetime, None] = None
    creator_id: int = 0
    created_at: datetime = common.now()


class FootprintCreateForm(BaseSchema):
    url: str
    action: str
    request_body: dict
    response_status_code: int
    response_body: str
    creator_id: int = 0
    created_at: datetime = common.now()


class DeviceCreateForm(BaseSchema):
    hostname: str
    asset_number: str
    ipv4_address: Union[str, None] = None
    ipv6_address: Union[str, None] = None
    mac_address: Union[str, None] = None
    description: Union[str, None] = None
    brand_id: int
    category_id: int
    creator_id: int = 0
    created_at: datetime = common.now()


# model schemas #
class Role(BaseSchema):
    id: int
    name: str
    scopes: list[str]
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]

    class Config:
        from_attributes = True


class User(BaseSchema):
    id: int
    username: str
    email: str
    name: str
    is_active: bool = True
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
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
    creator_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserHasRole(BaseSchema):
    id: int
    user_id: int
    role_id: int
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]

    class Config:
        from_attributes = True


class UserHasDevice(BaseSchema):
    id: int
    user_id: int
    device_id: int
    flag: int
    message: Union[str, None]
    expired_at: Union[datetime, None]
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]

    class Config:
        from_attributes = True


class Brand(BaseSchema):
    id: int
    name: str
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]

    class Config:
        from_attributes = True


class DeviceCategory(BaseSchema):
    id: int
    name: str
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]

    class Config:
        from_attributes = True


class Device(BaseSchema):
    id: int
    hostname: str
    asset_number: str
    ipv4_address: Union[str, None]
    ipv6_address: Union[str, None]
    mac_address: Union[str, None]
    description: Union[str, None]
    brand: Brand
    category: DeviceCategory
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]

    class Config:
        from_attributes = True
