from sqlalchemy import Boolean, Column, Integer, String, DateTime, JSON

from ..config.database import Base


class Footprint(Base):
    __tablename__ = "footprints"
    id = Column(Integer, primary_key=True, comment="ID")
    action = Column(String(255), comment="动作")
    url = Column(String(255), index=True, comment="请求地址")
    request_body = Column(JSON, nullable=True, comment="请求体")
    response_status_code = Column(Integer, comment="响应状态码")
    response_body = Column(JSON, nullable=True, comment="响应体")
    creator_id = Column(Integer, nullable=True, comment="创建者 ID")
    created_at = Column(DateTime, comment="创建时间")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, comment="ID")
    username = Column(String(255), unique=True, index=True, comment="用户名")
    email = Column(String(255), unique=True, index=True, comment="邮箱地址")
    name = Column(String(255), comment="名称")
    hashed_password = Column(String(255), comment="密码")
    is_active = Column(Boolean, default=True, comment="是否激活")
    creator_id = Column(Integer, nullable=True, comment="创建者 ID")
    created_at = Column(DateTime, nullable=True, comment="创建时间")
    deleted_at = Column(DateTime, nullable=True, comment="删除时间")


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, comment="ID")
    name = Column(String(255), unique=True, comment="名称")
    scopes = Column(JSON, comment="权限")
    creator_id = Column(Integer, nullable=True, comment="创建者 ID")
    created_at = Column(DateTime, nullable=True, comment="创建时间")
    deleted_at = Column(DateTime, nullable=True, comment="删除时间")


class UserHasRole(Base):
    __tablename__ = "user_has_roles"
    id = Column(Integer, primary_key=True, comment="ID")
    user_id = Column(Integer, comment="用户 ID")
    role_id = Column(Integer, comment="角色 ID")
    creator_id = Column(Integer, comment="创建者 ID")
    created_at = Column(DateTime, nullable=True, comment="创建时间")
    deleted_at = Column(DateTime, nullable=True, comment="删除时间")


class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, comment="ID")
    name = Column(String(255), unique=True, comment="名称")
    creator_id = Column(Integer, nullable=True, comment="创建者 ID")
    created_at = Column(DateTime, nullable=True, comment="创建时间")
    deleted_at = Column(DateTime, nullable=True, comment="删除时间")


class DeviceCategory(Base):
    __tablename__ = "device_categories"
    id = Column(Integer, primary_key=True, comment="ID")
    name = Column(String(255), unique=True, comment="名称")
    creator_id = Column(Integer, nullable=True, comment="创建者 ID")
    created_at = Column(DateTime, nullable=True, comment="创建时间")
    deleted_at = Column(DateTime, nullable=True, comment="删除时间")


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, comment="ID")
    hostname = Column(String(255), comment="主机名")
    asset_number = Column(String(255), unique=True, comment="资产编号")
    ipv4_address = Column(String(15), nullable=True, comment="IPv4 地址")
    ipv6_address = Column(String(39), nullable=True, comment="IPv6 地址")
    mac_address = Column(String(17), nullable=True, comment="MAC 地址")
    description = Column(String(255), nullable=True, comment="备注")
    brand_id = Column(Integer, comment="品牌 ID")
    category_id = Column(Integer, comment="分类 ID")
    creator_id = Column(Integer, comment="创建者 ID")
    created_at = Column(DateTime, nullable=True, comment="创建时间")
    deleted_at = Column(DateTime, nullable=True, comment="删除时间")


class UserHasDevice(Base):
    __tablename__ = "user_has_devices"
    id = Column(Integer, primary_key=True, comment="ID")
    user_id = Column(Integer, comment="用户 ID")
    device_id = Column(Integer, comment="设备 ID")
    flag = Column(Integer, comment="标识：-1归还1使用2借用")
    message = Column(String(255), nullable=True, comment="备注")
    expired_at = Column(DateTime, nullable=True, comment="到期时间")
    returned_at = Column(DateTime, nullable=True, comment="归还时间")
    creator_id = Column(Integer, nullable=True, comment="创建者 ID")
    created_at = Column(DateTime, nullable=True, comment="创建时间")
    deleted_at = Column(DateTime, nullable=True, comment="删除时间")
