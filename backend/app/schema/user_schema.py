# app/schemas/user_schema.py
from datetime import datetime
from typing import Optional, Literal
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    name: str
    email: str
    email_verified: bool = False
    image: Optional[str] = None
    role: Literal["user", "supervisor", "admin", "superAdmin"] = "user"
    banned: bool = False
    ban_reason: Optional[str] = None
    ban_expires: Optional[datetime] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Literal["user", "supervisor", "admin", "superAdmin"]] = None
    banned: Optional[bool] = None
    ban_reason: Optional[str] = None
    ban_expires: Optional[datetime] = None
