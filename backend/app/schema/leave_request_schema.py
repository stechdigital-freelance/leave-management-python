# app/schemas/leave_request_schema.py
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field


# --------------------------
# Base Schema
# --------------------------
class LeaveRequestBase(SQLModel):
    user_id: int = Field(..., foreign_key='"user".id')
    leave_type_id: int = Field(..., foreign_key="leave_types.id")
    project_id: Optional[int] = Field(default=None, foreign_key="projects.id")
    start_date: date
    end_date: date
    number_of_days: Decimal
    reason: Optional[str] = None
    status: Optional[str] = Field(
        default="pending",
        description="Leave status",
        max_length=20
    )
    comments: Optional[str] = None
    approved_rejected_at: Optional[datetime] = None
    approved_rejected_by: Optional[int] = Field(default=None, foreign_key='"user".id')


# --------------------------
# Create Schema
# --------------------------
class LeaveRequestCreate(LeaveRequestBase):
    """Schema for creating a new leave request."""
    pass


# --------------------------
# Update Schema
# --------------------------
class LeaveRequestUpdate(SQLModel):
    """Schema for updating an existing leave request."""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    number_of_days: Optional[Decimal] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    comments: Optional[str] = None
    approved_rejected_at: Optional[datetime] = None
    approved_rejected_by: Optional[int] = None
    project_id: Optional[int] = None


# --------------------------
# Read Schema
# --------------------------
class LeaveRequestRead(LeaveRequestBase):
    """Schema for reading leave requests."""
    id: int
    created_at: datetime
    updated_at: datetime
