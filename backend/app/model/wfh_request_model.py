# app/models/wfh_request_model.py
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.base_model import BaseModel


class WfhRequestBase(SQLModel):
    user_id: int = Field(..., foreign_key='"user".id')
    request_date: date
    reason: Optional[str] = None
    status: Optional[str] = Field(
        default="pending",
        description="WFH request status",
        sa_column_kwargs={
            "check_constraint": "status IN ('pending', 'approved', 'rejected', 'withdrawn', 'cancelled')"
        }
    )
    supervisor_id: Optional[int] = Field(default=None, foreign_key='"user".id')
    approved_rejected_at: Optional[datetime] = None
    approved_rejected_by: Optional[int] = Field(default=None, foreign_key='"user".id')
    comments: Optional[str] = None


class WfhRequest(WfhRequestBase, BaseModel, table=True):
    __tablename__ = "wfh_requests"

    # Relationships
    employee: "User" = Relationship(back_populates="wfh_requests")
    supervisor: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[WfhRequest.supervisor_id]"}
    )
    approved_rejected_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[WfhRequest.approved_rejected_by]"}
    )
