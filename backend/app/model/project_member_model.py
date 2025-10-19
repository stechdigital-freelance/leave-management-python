from datetime import date, datetime
from typing import Optional
from sqlalchemy.orm import SQLModel, Field, Relationship
from app.model.base_model import BaseModel

class ProjectMemberBase(SQLModel):
    project_id: int = Field(..., foreign_key="projects.id")
    user_id: int = Field(..., foreign_key='"user".id')
    role: str = Field(
        ...,
        sa_column_kwargs={"check_constraint": "role IN ('supervisor','co_supervisor','project_lead','team_member','contributor')"}
    )
    assignment_start_date: date
    assignment_end_date: Optional[date] = None
    is_active: bool = Field(default=True)

class ProjectMember(ProjectMemberBase, BaseModel, table=True):
    __tablename__ = "project_members"

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    project: "Project" = Relationship(back_populates="members")
    user: "User" = Relationship()
