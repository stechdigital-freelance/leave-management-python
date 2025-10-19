from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.base_model import BaseModel


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
        sa_column_kwargs={
            "check_constraint": "status IN ('pending', 'approved', 'rejected', 'withdrawn', 'cancelled')"
        }
    )
    comments: Optional[str] = None
    approved_rejected_at: Optional[datetime] = None
    approved_rejected_by: Optional[int] = Field(default=None, foreign_key='"user".id')


class LeaveRequest(LeaveRequestBase, BaseModel, table=True):
    __tablename__ = "leave_requests"

    # Relationships
    employee: "User" = Relationship(back_populates="leave_requests")
    leave_type: "LeaveType" = Relationship(back_populates="leave_requests")
    project: Optional["Project"] = Relationship()
    approved_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[LeaveRequest.approved_rejected_by]"})
