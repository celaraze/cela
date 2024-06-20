from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, JSON, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.database import Base


class Footprint(Base):
    __tablename__ = "footprints"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    action: Mapped[str] = mapped_column(String(255), comment="动作")
    url: Mapped[str] = mapped_column(String(255), index=True, comment="请求地址")
    request_body: Mapped[dict] = mapped_column(JSON, nullable=True, comment="请求体")
    response_status_code: Mapped[int] = mapped_column(Integer, comment="响应状态码")
    response_body: Mapped[dict] = mapped_column(JSON, nullable=True, comment="响应体")
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, comment="创建时间")
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="删除时间")


user_has_roles_table = Table(
    "user_has_roles",
    Base.metadata,
    Column("id", Integer, primary_key=True, comment="ID"),
    Column("user_id", Integer, ForeignKey("users.id"), comment="用户 ID"),
    Column("role_id", Integer, ForeignKey("roles.id"), comment="角色 ID"),
    Column("creator_id", Integer, comment="创建者 ID"),
    Column("created_at", DateTime, nullable=True, comment="创建时间"),
    Column("deleted_at", DateTime, nullable=True, comment="删除时间"),
)

user_has_devices_table = Table(
    "user_has_devices",
    Base.metadata,
    Column("id", Integer, primary_key=True, comment="ID"),
    Column("user_id", Integer, ForeignKey("users.id"), comment="用户 ID"),
    Column("device_id", Integer, ForeignKey("devices.id"), comment="设备 ID"),
    Column("flag", Integer, comment="标识：-1归还1使用2借用"),
    Column("message", String(255), nullable=True, comment="备注"),
    Column("expired_at", DateTime, nullable=True, comment="到期时间"),
    Column("status", Integer, comment="状态：0未结束1已结束"),
    Column("creator_id", Integer, comment="创建者 ID"),
    Column("created_at", DateTime, nullable=True, comment="创建时间"),
    Column("deleted_at", DateTime, nullable=True, comment="删除时间"),
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True, comment="用户名")
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, comment="邮箱地址")
    name: Mapped[str] = mapped_column(String(255), comment="名称")
    hashed_password: Mapped[str] = mapped_column(String(255), comment="密码")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否激活")
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="删除时间")

    roles: Mapped[list["Role"]] = relationship(secondary=user_has_roles_table)
    devices: Mapped[list["Device"]] = relationship(secondary=user_has_devices_table)


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    name: Mapped[str] = mapped_column(String(255), comment="名称")
    scopes: Mapped[list[str]] = mapped_column(JSON, comment="权限")
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="删除时间")

    users: Mapped[list["User"]] = relationship(secondary=user_has_roles_table)


class Brand(Base):
    __tablename__ = "brands"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    name: Mapped[str] = mapped_column(String(255), comment="名称")
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="删除时间")

    devices: Mapped[list["Device"]] = relationship(back_populates="brand")


class DeviceCategory(Base):
    __tablename__ = "device_categories"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    name: Mapped[str] = mapped_column(String(255), comment="名称")
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="删除时间")

    devices: Mapped[list["Device"]] = relationship(back_populates="device_category")


class Device(Base):
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
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="删除时间")

    brand: Mapped["Brand"] = relationship(back_populates="devices")
    device_category: Mapped["DeviceCategory"] = relationship(back_populates="devices")
    users: Mapped[list["User"]] = relationship(secondary=user_has_devices_table)
