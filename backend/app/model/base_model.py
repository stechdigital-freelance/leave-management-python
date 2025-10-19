from datetime import datetime
from typing import Optional
from sqlmodel import Column, DateTime, Field, SQLModel, func

class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    is_deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=True))