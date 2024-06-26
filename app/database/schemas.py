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


class AssetNumberCreateForm(BaseSchema):
    number: str
    table_name: str
    table_id: int
    creator_id: int = 0
    created_at: str = common.now()


class TicketCreateForm(BaseSchema):
    title: str
    description: str
    asset_number: Union[str, None] = None
    status: int = 0
    assignee_id: Union[int, None] = None
    priority: int = 0
    expired_at: Union[datetime, None] = None
    deleter_id: Union[int, None] = None
    creator_id: int = 0
    created_at: str = common.now()


class TicketCommentCreateForm(BaseSchema):
    ticket_id: int
    comment: str
    creator_id: int = 0
    created_at: str = common.now()


class TicketMinuteCreateForm(BaseSchema):
    ticket_id: int
    flag: int = 0
    message: Union[str, None] = None
    creator_id: int = 0
    created_at: str = common.now()


class TodoCreateForm(BaseSchema):
    title: str
    priority: int = 0
    expired_at: Union[datetime, None] = None
    is_finished: bool = False
    finished_at: Union[datetime, None] = None
    creator_id: int = 0
    created_at: str = common.now()


class TodoMinuteCreateForm(BaseSchema):
    todo_id: int
    flag: int = 0
    is_finished: int = 0
    creator_id: int = 0
    created_at: str = common.now()


# Model schemas.
class Creator(BaseSchema):
    id: int
    name: str
    username: str
    email: str
    is_active: bool


class Deleter(BaseSchema):
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


class UserHistoricalRole(BaseSchema):
    id: int
    role_id: int
    role_name: str
    role_scopes: list[str]
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None

    class ConfigDict:
        from_attributes = True


class RoleHistoricalUser(BaseSchema):
    id: int
    user_id: int
    user_name: str
    user_username: str
    user_email: str
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None

    class ConfigDict:
        from_attributes = True


class DeviceHistoricalUser(BaseSchema):
    id: int
    user_id: int
    user_name: str
    user_username: str
    user_email: str
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None

    class ConfigDict:
        from_attributes = True


class UserHistoricalDevice(BaseSchema):
    id: int
    device_id: int
    device_hostname: str
    device_asset_number: str
    device_description: Union[str, None]
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


class RoleForUser(BaseSchema):
    id: int
    name: str
    scopes: list[str]

    # This is not user's created_at, but user_has_device's created_at.
    created_at: Union[datetime, None]
    # This is not user's deleted_at, but user_has_device's deleted_at.
    deleted_at: Union[datetime, None]

    class ConfigDict:
        from_attributes = True


class UserForRole(BaseSchema):
    id: int
    username: str
    email: str
    name: str
    is_active: bool = True

    # This is not user's created_at, but user_has_device's created_at.
    created_at: Union[datetime, None]
    # This is not user's deleted_at, but user_has_device's deleted_at.
    deleted_at: Union[datetime, None]

    class ConfigDict:
        from_attributes = True


class UserForDevice(BaseSchema):
    id: int
    username: str
    email: str
    name: str
    is_active: bool = True

    # This is not user's created_at, but user_has_device's created_at.
    created_at: Union[datetime, None]
    # This is not user's deleted_at, but user_has_device's deleted_at.
    deleted_at: Union[datetime, None]

    class ConfigDict:
        from_attributes = True


class DeviceForUser(BaseSchema):
    id: int
    hostname: str
    asset_number: str
    ipv4_address: Union[str, None]
    ipv6_address: Union[str, None]
    mac_address: Union[str, None]
    description: Union[str, None]

    # This is not device's created_at, but user_has_device's created_at.
    created_at: Union[datetime, None]
    # This is not device's deleted_at, but user_has_device's deleted_at.
    deleted_at: Union[datetime, None]

    brand: Union[Brand, None] = None
    category: Union[DeviceCategory, None] = None

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
    users: Union["User", None] = None

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


class AssetNumber(BaseSchema):
    id: int
    number: str
    table_name: str
    table_id: int
    creator_id: int
    created_at: Union[datetime, None]

    class ConfigDict:
        from_attributes = True


class Ticket(BaseSchema):
    id: int
    title: str
    description: str
    asset_number: Union[str, None]
    status: int
    assignee_id: Union[int, None]
    priority: int
    expired_at: Union[datetime, None]
    deleter_id: Union[int, None]
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None
    deleter: Union[Deleter, None] = None

    comments: list["TicketComment"] = []
    minutes: list["TicketMinute"] = []

    class ConfigDict:
        from_attributes = True


class TicketComment(BaseSchema):
    id: int
    ticket_id: int
    comment: str
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None

    class ConfigDict:
        from_attributes = True


class TicketMinute(BaseSchema):
    id: int
    ticket_id: int
    flag: int
    message: Union[str, None]
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]

    class ConfigDict:
        from_attributes = True


class Todo(BaseSchema):
    id: int
    title: str
    priority: int
    expired_at: Union[datetime, None]
    is_finished: bool
    finished_at: Union[datetime, None]
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]
    creator: Union[Creator, None] = None

    minutes: list["TodoMinute"] = []

    class ConfigDict:
        from_attributes = True


class TodoMinute(BaseSchema):
    id: int
    todo_id: int
    flag: int
    is_finished: int
    creator_id: int
    created_at: Union[datetime, None]
    deleted_at: Union[datetime, None]

    class ConfigDict:
        from_attributes = True
