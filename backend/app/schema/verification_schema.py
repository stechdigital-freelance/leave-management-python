# app/schemas/verification_schema.py
from datetime import datetime
from sqlmodel import SQLModel, Field


class VerificationBase(SQLModel):
    identifier: str
    value: str
    expires_at: datetime


class VerificationRead(VerificationBase):
    id: int
    created_at: datetime
    updated_at: datetime


class VerificationCreate(VerificationBase):
    pass
