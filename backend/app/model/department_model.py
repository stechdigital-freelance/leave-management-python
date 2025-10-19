# app/models/department_model.py
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.model.base_model import BaseModel


class DepartmentBase(SQLModel):
    name: str = Field(..., min_length=1, max_length=100, description="Department name")
    description: Optional[str] = Field(None, description="Department description")


class Department(DepartmentBase, BaseModel, table=True):
    __tablename__ = "departments"

    # One-to-many relationship with Project
    projects: List["Project"] = Relationship(back_populates="department")
