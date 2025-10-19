# app/models/project_model.py
from datetime import date, datetime
from typing import Optional, Literal
from sqlmodel import SQLModel, Field, Relationship
from app.model.base_model import BaseModel


class ProjectBase(SQLModel):
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    code: str = Field(..., min_length=1, max_length=20, description="Unique project code")
    description: Optional[str] = Field(None, description="Project description")
    department_id: Optional[int] = Field(default=None, foreign_key="departments.id")
    start_date: Optional[date] = Field(default=None, description="Project start date")
    end_date: Optional[date] = Field(default=None, description="Project end date")
    status: Optional[Literal["active", "completed", "on_hold", "cancelled"]] = Field(
        default="active", description="Current project status"
    )


class Project(ProjectBase, BaseModel, table=True):
    __tablename__ = "projects"

    # Relationships (optional, if you want to easily access the linked Department)
    department: Optional["Department"] = Relationship(back_populates="projects")
