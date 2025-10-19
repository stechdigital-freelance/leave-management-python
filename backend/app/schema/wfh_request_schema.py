# app/schemas/wfh_request_schema.py
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field


class WfhRequestBase(SQLModel):
    user_id: int = Field(..., foreign_key='"user".id')
    request_date: date
    reason: Optional[str] = None
    status: Optional[str] = Field(
        default="pending",
        description="WFH request status"
    )
    supervisor_id: Optional[int] = Field(default=None, foreign_key='"user".id')
    approved_rejected_at: Optional[datetime] = None
    approved_rejected_by: Optional[int] = Field(default=None, foreign_key='"user".id')
    comments: Optional[str] = None



class WfhRequestCreate(WfhRequestBase):
    """Schema for creating a new WFH request."""
    pass



class WfhRequestUpdate(SQLModel):

    request_date: Optional[date] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    supervisor_id: Optional[int] = None
    approved_rejected_at: Optional[datetime] = None
    approved_rejected_by: Optional[int] = None
    comments: Optional[str] = None



class WfhRequestRead(WfhRequestBase):
   
    id: int
    created_at: datetime
    updated_at: datetime
