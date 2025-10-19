# app/schemas/account_schema.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class AccountBase(SQLModel):
    user_id: int
    account_id: str
    provider_id: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    access_token_expires_at: Optional[datetime] = None
    refresh_token_expires_at: Optional[datetime] = None
    scope: Optional[str] = None
    id_token: Optional[str] = None
    password: Optional[str] = None


class AccountRead(AccountBase):
    id: int
    created_at: datetime
    updated_at: datetime


class AccountCreate(AccountBase):
    pass


class AccountUpdate(SQLModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    password: Optional[str] = None
