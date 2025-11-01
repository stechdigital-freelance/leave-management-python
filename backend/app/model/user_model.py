# app/models/user_model.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List, Literal
from uuid import UUID
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import text
from sqlalchemy import CheckConstraint
from app.model.base import Base

if TYPE_CHECKING:
    from app.model.department_model import DepartmentAdmin


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        unique=True, 
        nullable=False,
        index=True,
        server_default=text("uuidv7()")  # PostgreSQL UUID v7
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        String(20),
        default="user",
        nullable=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("NOW()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("NOW()"),
        onupdate=text("NOW()")
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "role IN ('user', 'supervisor', 'admin', 'superAdmin')",
            name="check_user_role",
        ),
    )

    # Relationships
    # department_admins: Mapped[List["DepartmentAdmin"]] = relationship(
    #     "DepartmentAdmin", 
    #     back_populates="user"
    # )
    department_admins = relationship(
        "DepartmentAdmin",
        back_populates="user",
    )


    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"

from app.model.department_model import DepartmentAdmin  # noqa

# class User(Base):
#     __tablename__ = "user"

#     # Columns
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     email: Mapped[str] = mapped_column(String(255), nullable=False)
#     email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
#     image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     role: Mapped[str] = mapped_column(
#         String(20),
#         default="user",
#         nullable=False
#     )
#     banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
#     ban_reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     ban_expires: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

#     # Constraints
#     __table_args__ = (
#         CheckConstraint(
#             "role IN ('user', 'supervisor', 'admin', 'superAdmin')",
#             name="check_user_role",
#         ),
#     )

#     # Relationships
#     sessions: Mapped[List["Session"]] = relationship("Session", back_populates="user")
#     accounts: Mapped[List["Account"]] = relationship("Account", back_populates="user")
#     impersonations: Mapped[List["Session"]] = relationship(
#         "Session",
#         back_populates="impersonator",
#         foreign_keys="[Session.impersonated_by]",
#     )
#     attendance_records: Mapped[List["AttendanceRecord"]] = relationship("AttendanceRecord", back_populates="user")
#     leave_requests: Mapped[List["LeaveRequest"]] = relationship("LeaveRequest", back_populates="employee")
#     wfh_requests: Mapped[List["WfhRequest"]] = relationship("WfhRequest", back_populates="user")

#     department_admins: Mapped[list["DepartmentAdmin"]] = relationship(
#         "DepartmentAdmin", 
#         back_populates="user"
#     )
