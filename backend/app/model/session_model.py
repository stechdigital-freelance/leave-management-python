# app/models/session_model.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.base_model import BaseModel


class SessionBase(SQLModel):
    user_id: int = Field(..., foreign_key="user.id")
    token: str = Field(..., description="Session token")
    expires_at: datetime = Field(..., description="When the session expires")
    ip_address: Optional[str] = Field(default=None, description="User IP address")
    user_agent: Optional[str] = Field(default=None, description="User agent")
    impersonated_by: Optional[int] = Field(default=None, foreign_key="user.id")


class Session(SessionBase, BaseModel, table=True):
    __tablename__ = "session"

    user: "User" = Relationship(back_populates="sessions", sa_relationship_kwargs={"foreign_keys": "[Session.user_id]"})
    impersonator: Optional["User"] = Relationship(
        back_populates="impersonations",
        sa_relationship_kwargs={"foreign_keys": "[Session.impersonated_by]"},
    )
