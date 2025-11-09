# app/schemas/project_schema.py
from datetime import datetime, date
from typing import Optional, Literal
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    code: str = Field(..., min_length=1, max_length=20, description="Unique project code")
    description: Optional[str] = Field(None, description="Project description")
    department_id: Optional[int] = Field(None, description="Linked department ID")
    start_date: Optional[date] = Field(None, description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end date")
    status: Optional[Literal["active", "completed", "on_hold", "cancelled"]] = Field(
        default="active", description="Current project status"
    )


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Enables ORM-to-Pydantic conversion for SQLModel/SQLAlchemy


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    department_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[Literal["active", "completed", "on_hold", "cancelled"]] = None
