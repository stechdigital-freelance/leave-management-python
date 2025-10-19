# app/schemas/attendance_record_schema.py
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field


# --------------------------
# Base Schema
# --------------------------
class AttendanceRecordBase(SQLModel):
    user_id: int = Field(..., foreign_key='"user".id')
    work_date: date
    work_month: Optional[int] = None
    work_year: Optional[int] = None

    time_in: Optional[datetime] = None
    time_out: Optional[datetime] = None

    break1_start: Optional[datetime] = None
    break1_end: Optional[datetime] = None
    break2_start: Optional[datetime] = None
    break2_end: Optional[datetime] = None
    break3_start: Optional[datetime] = None
    break3_end: Optional[datetime] = None

    source_system: Optional[str] = Field(default=None, max_length=100)
    work_mode: Optional[str] = Field(default=None, max_length=50)
    is_active: bool = Field(default=True)


# --------------------------
# Create Schema
# --------------------------
class AttendanceRecordCreate(AttendanceRecordBase):
    """Used when creating a new attendance record."""
    pass


# --------------------------
# Update Schema
# --------------------------
class AttendanceRecordUpdate(SQLModel):
    """Used for partial updates (PATCH)."""
    work_date: Optional[date] = None
    time_in: Optional[datetime] = None
    time_out: Optional[datetime] = None

    break1_start: Optional[datetime] = None
    break1_end: Optional[datetime] = None
    break2_start: Optional[datetime] = None
    break2_end: Optional[datetime] = None
    break3_start: Optional[datetime] = None
    break3_end: Optional[datetime] = None

    source_system: Optional[str] = Field(default=None, max_length=100)
    work_mode: Optional[str] = Field(default=None, max_length=50)
    is_active: Optional[bool] = None


# --------------------------
# Read Schema
# --------------------------
class AttendanceRecordRead(AttendanceRecordBase):
    """Used for reading attendance records."""
    id: int
    created_at: datetime
    updated_at: datetime
