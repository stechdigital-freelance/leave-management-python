# app/models/department.py
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.model.base import Base

if TYPE_CHECKING:
    from app.model.user_model import User


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    # Relationships
    admins: Mapped[list["DepartmentAdmin"]] = relationship(
        "DepartmentAdmin", 
        back_populates="department",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}', code='{self.code}')>"


class DepartmentAdmin(Base):
    __tablename__ = "department_admins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"), 
        nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    # Relationships
    department: Mapped["Department"] = relationship(
        "Department", 
        back_populates="admins"
    )
    user: Mapped["User"] = relationship("User", back_populates="department_admins")

    __table_args__ = (
        UniqueConstraint('department_id', 'user_id', name='uq_department_user'),
    )

    def __repr__(self):
        return f"<DepartmentAdmin(id={self.id}, department_id={self.department_id}, user_id='{self.user_id}')>"
