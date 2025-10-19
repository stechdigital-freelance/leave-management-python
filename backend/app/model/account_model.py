# app/models/account_model.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.base_model import BaseModel


class AccountBase(SQLModel):
    user_id: int = Field(..., foreign_key="user.id")
    account_id: str = Field(..., max_length=255)
    provider_id: str = Field(..., max_length=100)
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    access_token_expires_at: Optional[datetime] = None
    refresh_token_expires_at: Optional[datetime] = None
    scope: Optional[str] = None
    id_token: Optional[str] = None
    password: Optional[str] = None


class Account(AccountBase, BaseModel, table=True):
    __tablename__ = "account"

    user: "User" = Relationship(back_populates="accounts")
