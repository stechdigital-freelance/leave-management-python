# app/models/user_model.py
from datetime import datetime
from typing import Optional, List, Literal

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy.sql import text
from sqlalchemy import CheckConstraint

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(
        String(20),
        default="user",
        nullable=False
    )
    banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ban_reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ban_expires: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "role IN ('user', 'supervisor', 'admin', 'superAdmin')",
            name="check_user_role",
        ),
    )

    # Relationships
    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="user")
    accounts: Mapped[List["Account"]] = relationship("Account", back_populates="user")
    impersonations: Mapped[List["Session"]] = relationship(
        "Session",
        back_populates="impersonator",
        foreign_keys="[Session.impersonated_by]",
    )
    attendance_records: Mapped[List["AttendanceRecord"]] = relationship("AttendanceRecord", back_populates="user")
    leave_requests: Mapped[List["LeaveRequest"]] = relationship("LeaveRequest", back_populates="employee")
    wfh_requests: Mapped[List["WfhRequest"]] = relationship("WfhRequest", back_populates="user")
