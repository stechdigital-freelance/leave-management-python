# app/models/leave_type_model.py
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.model.base_model import BaseModel


class LeaveTypeBase(SQLModel):
    name: str = Field(..., max_length=50)
    code: str = Field(..., max_length=20)
    description: Optional[str] = None
    max_days_per_year: int = Field(default=0)
    can_carry_forward: bool = Field(default=False)
    is_active: bool = Field(default=True)


class LeaveType(LeaveTypeBase, BaseModel, table=True):
    __tablename__ = "leave_types"

    # Relationships
    leave_requests: List["LeaveRequest"] = Relationship(back_populates="leave_type")
    employee_balances: List["EmployeeLeaveBalance"] = Relationship(back_populates="leave_type")
