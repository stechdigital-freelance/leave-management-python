# app/schemas/employee_leave_balance_schema.py
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field


class EmployeeLeaveBalanceBase(SQLModel):
    employee_id: int
    leave_type_id: int
    year: int
    total_days: int
    used_days: int = 0
    carried_forward_days: int = 0
    carry_forward_expiry_date: Optional[date] = None


class EmployeeLeaveBalanceCreate(EmployeeLeaveBalanceBase):
    pass


class EmployeeLeaveBalanceRead(EmployeeLeaveBalanceBase):
    id: int
    created_at: datetime
    updated_at: datetime


class EmployeeLeaveBalanceUpdate(SQLModel):
    total_days: Optional[int] = None
    used_days: Optional[int] = None
    carried_forward_days: Optional[int] = None
    carry_forward_expiry_date: Optional[date] = None
