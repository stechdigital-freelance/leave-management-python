# app/schemas/session_schema.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class SessionBase(SQLModel):
    user_id: int
    token: str
    expires_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    impersonated_by: Optional[int] = None


class SessionRead(SessionBase):
    id: int
    created_at: datetime
    updated_at: datetime


class SessionCreate(SessionBase):
    pass


class SessionUpdate(SQLModel):
    expires_at: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
