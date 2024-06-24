from datetime import datetime

from sqlalchemy import Boolean, Integer, String, DateTime, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Additions:
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="创建者 ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="创建时间")
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="删除时间")


class Footprint(Base, Additions):
    __tablename__ = "footprints"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    action: Mapped[str] = mapped_column(String(255), comment="动作")
    url: Mapped[str] = mapped_column(String(255), index=True, comment="请求地址")
    request_body: Mapped[dict] = mapped_column(JSON, nullable=True, comment="请求体")
    response_status_code: Mapped[int] = mapped_column(Integer, comment="响应状态码")
    response_body: Mapped[dict] = mapped_column(JSON, nullable=True, comment="响应体")


class UserHasRole(Base, Additions):
    __tablename__ = "user_has_roles"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    user_id: Mapped[int] = mapped_column(Integer, comment="用户 ID")
    role_id: Mapped[int] = mapped_column(Integer, comment="角色 ID")


class UserHasDevice(Base, Additions):
    __tablename__ = "user_has_devices"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    user_id: Mapped[int] = mapped_column(Integer, comment="用户 ID")
    device_id: Mapped[int] = mapped_column(Integer, comment="设备 ID")
    flag: Mapped[int] = mapped_column(Integer, comment="标识：-1归还1使用2借用")
    message: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注")
    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="到期时间")
    status: Mapped[int] = mapped_column(Integer, comment="状态：0未结束1已结束")


class User(Base, Additions):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True, comment="用户名")
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, comment="邮箱地址")
    name: Mapped[str] = mapped_column(String(255), comment="名称")
    hashed_password: Mapped[str] = mapped_column(String(255), comment="密码")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否激活")


class Role(Base, Additions):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    name: Mapped[str] = mapped_column(String(255), comment="名称")
    scopes: Mapped[list[str]] = mapped_column(JSON, comment="权限")


class Brand(Base, Additions):
    __tablename__ = "brands"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    name: Mapped[str] = mapped_column(String(255), comment="名称")


class DeviceCategory(Base, Additions):
    __tablename__ = "device_categories"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    name: Mapped[str] = mapped_column(String(255), comment="名称")


class Device(Base, Additions):
    __tablename__ = "devices"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    hostname: Mapped[str] = mapped_column(String(255), comment="主机名")
    asset_number: Mapped[str] = mapped_column(String(255), index=True, comment="资产编号")
    ipv4_address: Mapped[str] = mapped_column(String(15), nullable=True, comment="IPv4 地址")
    ipv6_address: Mapped[str] = mapped_column(String(39), nullable=True, comment="IPv6 地址")
    mac_address: Mapped[str] = mapped_column(String(17), nullable=True, comment="MAC 地址")
    description: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注")
    brand_id: Mapped[int] = mapped_column(Integer, comment="品牌 ID")
    category_id: Mapped[int] = mapped_column(Integer, comment="分类 ID")


class AssetNumber(Base, Additions):
    __tablename__ = "asset_numbers"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    number: Mapped[str] = mapped_column(String(255), index=True, comment="编号")
    table_name: Mapped[str] = mapped_column(String(255), comment="表名")
    table_id: Mapped[int] = mapped_column(Integer, comment="表 ID")


class Ticket(Base, Additions):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    title: Mapped[str] = mapped_column(String(255), comment="标题")
    description: Mapped[str] = mapped_column(Text, comment="描述")
    asset_number: Mapped[str] = mapped_column(String(255), nullable=True, comment="资产编号")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="状态：0空闲1处理2完成3关闭")
    assignee_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="指派者 ID")
    priority: Mapped[int] = mapped_column(Integer, comment="优先级")
    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="到期时间")
    deleter_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="删除者 ID")


class TicketComment(Base, Additions):
    __tablename__ = "ticket_comments"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    ticket_id: Mapped[int] = mapped_column(Integer, comment="工单 ID")
    comment: Mapped[str] = mapped_column(Text, nullable=True, comment="评论")


class TicketMinute(Base, Additions):
    __tablename__ = "ticket_minutes"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    ticket_id: Mapped[int] = mapped_column(Integer, comment="工单 ID")
    flag: Mapped[int] = mapped_column(Integer, default=0, comment="标识：0开始1结束")
    message: Mapped[str] = mapped_column(Text, nullable=True, comment="备注")


class Todo(Base, Additions):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    title: Mapped[str] = mapped_column(String(255), comment="标题")
    priority: Mapped[int] = mapped_column(Integer, comment="优先级,0低1中2高3紧急")
    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="到期时间")
    is_finished: Mapped[int] = mapped_column(Integer, default=0, comment="状态：0未完成1已完成")
    finished_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="完成时间")


class TodoMinute(Base, Additions):
    __tablename__ = "todo_minutes"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    todo_id: Mapped[int] = mapped_column(Integer, comment="待办 ID")
    flag: Mapped[int] = mapped_column(Integer, default=0, comment="标识：0开始1结束")
    is_finished: Mapped[int] = mapped_column(Integer, default=0, comment="状态：0未完成1已完成")
