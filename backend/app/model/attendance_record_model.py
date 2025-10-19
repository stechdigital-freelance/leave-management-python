# app/models/attendance_record_model.py
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.base_model import BaseModel


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


class AttendanceRecord(AttendanceRecordBase, BaseModel, table=True):
    __tablename__ = "attendance_records"

    # Relationships
    user: "User" = Relationship(back_populates="attendance_records")
