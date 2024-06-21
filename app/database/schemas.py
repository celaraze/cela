from datetime import datetime
from typing import Union, Any

from pydantic import BaseModel as BaseSchema

from app.utils import common


# schema for decoding token
class AuthTokenData(BaseSchema):
    user_id: int
    scopes: list[str] = []


# Form schemas.

class UpdateForm(BaseSchema):
    key: str
    value: Any


class QueryForm(BaseSchema):
    key: str
    operator: str
    value: Any


class RoleCreateForm(BaseSchema):
    name: str
    scopes: list[str] = []
    creator_id: int = 0
    created_at: str = common.now()


class UserChangePasswordForm(BaseSchema):
    old_password: str
    new_password: str


class UserCreateForm(BaseSchema):
    username: str
    email: str
    name: str
    password: Union[str, None] = None
    hashed_password: Union[str, None] = None
    creator_id: int = 0
    created_at: str = common.now()


class BrandCreateForm(BaseSchema):
    name: str
    creator_id: int = 0
    created_at: str = common.now()


class DeviceCategoryCreateForm(BaseSchema):
    name: str
    creator_id: int = 0
    created_at: str = common.now()


class UserHasRoleCreateForm(BaseSchema):
    user_id: int
    role_id: int
    creator_id: int = 0
    created_at: str = common.now()


class UserHasDeviceCreateOrUpdateForm(BaseSchema):
    user_id: int
    device_id: int
    flag: int = 0
    message: Union[str, None] = None
    expired_at: Union[datetime, None] = None
    status: int = 0
    creator_id: int = 0
    created_at: str = common.now()
    deleted_at: Union[datetime, None] = None


class FootprintCreateForm(BaseSchema):
    url: str
    action: str
    request_body: dict
    response_status_code: int
    response_body: str
    creator_id: int = 0
    created_at: str = common.now()


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
    created_at: str = common.now()


# Model schemas.
class Creator(BaseSchema):
    id: int
    name: str
    username: str
    email: str
    is_active: bool


class Role(BaseSchema):
    id: int
    name: str
    scopes: list[str]
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None
    users: list["User"] = []

    class ConfigDict:
        from_attributes = True


class Footprint(BaseSchema):
    id: int
    url: str
    action: str
    request_body: dict
    response_status_code: int
    response_body: dict
    creator_id: int
    created_at: str
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None

    class ConfigDict:
        from_attributes = True


class UserHasRole(BaseSchema):
    id: int
    user_id: int
    role_id: int
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None

    class ConfigDict:
        from_attributes = True


class UserHasDevice(BaseSchema):
    id: int
    user_id: int
    device_id: int
    flag: int
    message: Union[str, None]
    expired_at: Union[datetime, None]
    status: int
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None

    class ConfigDict:
        from_attributes = True


class Brand(BaseSchema):
    id: int
    name: str
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None

    class ConfigDict:
        from_attributes = True


class DeviceCategory(BaseSchema):
    id: int
    name: str
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None

    class ConfigDict:
        from_attributes = True


class UserForRole(BaseSchema):
    id: int
    username: str
    email: str
    name: str
    is_active: bool = True

    class ConfigDict:
        from_attributes = True


class UserForDevice(BaseSchema):
    id: int
    username: str
    email: str
    name: str
    is_active: bool = True

    class ConfigDict:
        from_attributes = True


class Device(BaseSchema):
    id: int
    hostname: str
    asset_number: str
    ipv4_address: Union[str, None]
    ipv6_address: Union[str, None]
    mac_address: Union[str, None]
    description: Union[str, None]
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None

    brand: Union[Brand, None] = None
    category: Union[DeviceCategory, None] = None
    users: list["User"] = []

    class ConfigDict:
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
    creator: Union[Creator, None] = None
    roles: list[Role] = []
    scopes: list[str] = []
    devices: list[Device] = []

    class ConfigDict:
        from_attributes = True
