# app/models/verification_model.py
from datetime import datetime
from sqlmodel import SQLModel, Field
from app.model.base_model import BaseModel


class VerificationBase(SQLModel):
    identifier: str = Field(..., max_length=255)
    value: str = Field(...)
    expires_at: datetime = Field(...)


class Verification(VerificationBase, BaseModel, table=True):
    __tablename__ = "verification"
