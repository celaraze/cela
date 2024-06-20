from datetime import datetime

from sqlalchemy import Boolean, Integer, String, DateTime, JSON, ForeignKey, event, orm
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session

from app.database.database import Base


class SoftDelete:
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="删除时间")


class Footprint(Base, SoftDelete):
    __tablename__ = "footprints"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    action: Mapped[str] = mapped_column(String(255), comment="动作")
    url: Mapped[str] = mapped_column(String(255), index=True, comment="请求地址")
    request_body: Mapped[dict] = mapped_column(JSON, nullable=True, comment="请求体")
    response_status_code: Mapped[int] = mapped_column(Integer, comment="响应状态码")
    response_body: Mapped[dict] = mapped_column(JSON, nullable=True, comment="响应体")
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, comment="创建时间")


class UserHasRole(Base, SoftDelete):
    __tablename__ = "user_has_roles"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), comment="用户 ID")
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), comment="角色 ID")
    creator_id: Mapped[int] = mapped_column(Integer, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")

    role: Mapped["Role"] = relationship("Role", back_populates="user_has_roles")
    user: Mapped["User"] = relationship("User", back_populates="user_has_roles")


class UserHasDevice(Base, SoftDelete):
    __tablename__ = "user_has_devices"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), comment="用户 ID")
    device_id: Mapped[int] = mapped_column(Integer, ForeignKey("devices.id"), comment="设备 ID")
    flag: Mapped[int] = mapped_column(Integer, comment="标识：-1归还1使用2借用")
    message: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注")
    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="到期时间")
    status: Mapped[int] = mapped_column(Integer, comment="状态：0未结束1已结束")
    creator_id: Mapped[int] = mapped_column(Integer, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")

    device: Mapped["Device"] = relationship("Device", back_populates="user_has_devices")
    user: Mapped["User"] = relationship("User", back_populates="user_has_devices")


class User(Base, SoftDelete):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True, comment="用户名")
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, comment="邮箱地址")
    name: Mapped[str] = mapped_column(String(255), comment="名称")
    hashed_password: Mapped[str] = mapped_column(String(255), comment="密码")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否激活")
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")

    roles: Mapped[list["Role"]] = relationship(secondary=UserHasRole.__table__, back_populates="users")
    user_has_roles: Mapped[list["UserHasRole"]] = relationship("UserHasRole", back_populates="user")

    devices: Mapped[list["Device"]] = relationship(secondary=UserHasDevice.__table__, back_populates="users")
    user_has_devices: Mapped[list["UserHasDevice"]] = relationship("UserHasDevice", back_populates="user")


class Role(Base, SoftDelete):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    name: Mapped[str] = mapped_column(String(255), comment="名称")
    scopes: Mapped[list[str]] = mapped_column(JSON, comment="权限")
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")

    users: Mapped[list["User"]] = relationship(secondary=UserHasRole.__table__, back_populates="roles")
    user_has_roles: Mapped[list["UserHasRole"]] = relationship("UserHasRole", back_populates="role")


class Brand(Base, SoftDelete):
    __tablename__ = "brands"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    name: Mapped[str] = mapped_column(String(255), comment="名称")
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")

    devices: Mapped[list["Device"]] = relationship(back_populates="brand")


class DeviceCategory(Base, SoftDelete):
    __tablename__ = "device_categories"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    name: Mapped[str] = mapped_column(String(255), comment="名称")
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")

    devices: Mapped[list["Device"]] = relationship(back_populates="device_category")


class Device(Base, SoftDelete):
    __tablename__ = "devices"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    hostname: Mapped[str] = mapped_column(String(255), comment="主机名")
    asset_number: Mapped[str] = mapped_column(String(255), unique=True, comment="资产编号")
    ipv4_address: Mapped[str] = mapped_column(String(15), nullable=True, comment="IPv4 地址")
    ipv6_address: Mapped[str] = mapped_column(String(39), nullable=True, comment="IPv6 地址")
    mac_address: Mapped[str] = mapped_column(String(17), nullable=True, comment="MAC 地址")
    description: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注")
    brand_id: Mapped[int] = mapped_column(Integer, ForeignKey("brands.id"), comment="品牌 ID")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("device_categories.id"), comment="分类 ID")
    creator_id: Mapped[int] = mapped_column(Integer, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")

    brand: Mapped["Brand"] = relationship(back_populates="devices")
    device_category: Mapped["DeviceCategory"] = relationship(back_populates="devices")

    users: Mapped[list["User"]] = relationship(secondary=UserHasDevice.__table__, back_populates="devices")
    user_has_devices: Mapped[list["UserHasDevice"]] = relationship("UserHasDevice", back_populates="device")
