from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel

# --------------------------
# Base Schema
# --------------------------
class ProjectMemberBase(SQLModel):
    project_id: int
    user_id: int
    role: str = "team_member"
    assignment_start_date: date
    assignment_end_date: Optional[date] = None
    is_active: Optional[bool] = True


# --------------------------
# Create Schema
# --------------------------
class ProjectMemberCreate(ProjectMemberBase):
    """Schema for creating a new project member."""
    pass


# --------------------------
# Update Schema
# --------------------------
class ProjectMemberUpdate(SQLModel):
    """Schema for updating an existing project member."""
    role: Optional[str] = None
    assignment_start_date: Optional[date] = None
    assignment_end_date: Optional[date] = None
    is_active: Optional[bool] = None


# --------------------------
# Read Schema
# --------------------------
class ProjectMemberRead(ProjectMemberBase):
    """Schema for reading project members."""
    id: int
    created_at: datetime
    updated_at: datetime
