from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship

from ..config.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, comment="ID")
    username = Column(String(255), unique=True, index=True, comment="用户名")
    email = Column(String(255), unique=True, index=True, comment="邮箱地址")
    name = Column(String(255), comment="名称")
    hashed_password = Column(String(255), comment="密码")
    is_active = Column(Boolean, default=True, comment="是否激活")
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="操作人ID")
    created_at = Column(DateTime, nullable=True, comment="创建时间")
    deleted_at = Column(DateTime, nullable=True, comment="删除时间")

    # 远程一对多关系，用户有多个角色，通过中间表 user_has_roles 绑定
    roles = relationship("Role", secondary="user_has_roles", back_populates="users")
    # 一对一关系，用户有一个操作人，操作人也是用户，相当于自关联
    creator = relationship("User", remote_side=id)  # type: ignore # TODO


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, comment="ID")
    name = Column(String(255), unique=True, comment="名称")
    scopes = Column(JSON, comment="权限")

    users = relationship("User", secondary="user_has_roles", back_populates="roles")


class UserHasRole(Base):
    __tablename__ = "user_has_roles"
    id = Column(Integer, primary_key=True, comment="ID")
    user_id = Column(Integer, ForeignKey("users.id"), comment="用户 ID")
    role_id = Column(Integer, ForeignKey("roles.id"), comment="角色 ID")
