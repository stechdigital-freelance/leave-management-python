# app/schemas/leave_type_schema.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class LeaveTypeBase(SQLModel):
    name: str
    code: str
    description: Optional[str] = None
    max_days_per_year: int = 0
    can_carry_forward: bool = False
    is_active: bool = True


class LeaveTypeCreate(LeaveTypeBase):
    pass


class LeaveTypeRead(LeaveTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime


class LeaveTypeUpdate(SQLModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    max_days_per_year: Optional[int] = None
    can_carry_forward: Optional[bool] = None
    is_active: Optional[bool] = None
