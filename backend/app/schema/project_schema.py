# app/schemas/project_schema.py
from datetime import datetime, date
from typing import Optional, Literal
from sqlmodel import SQLModel, Field


class ProjectBase(SQLModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    department_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[Literal["active", "completed", "on_hold", "cancelled"]] = "active"


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(SQLModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    department_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[Literal["active", "completed", "on_hold", "cancelled"]] = None
