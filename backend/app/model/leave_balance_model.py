# app/models/employee_leave_balance_model.py
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.base_model import BaseModel


class EmployeeLeaveBalanceBase(SQLModel):
    employee_id: int = Field(..., foreign_key='"user".id')
    leave_type_id: int = Field(..., foreign_key="leave_types.id")
    year: int
    total_days: int
    used_days: int = Field(default=0)
    carried_forward_days: int = Field(default=0)
    carry_forward_expiry_date: Optional[date] = None


class EmployeeLeaveBalance(EmployeeLeaveBalanceBase, BaseModel, table=True):
    __tablename__ = "employee_leave_balance"

    # Relationships
    leave_type: "LeaveType" = Relationship(back_populates="employee_balances")
    employee: "User" = Relationship()
