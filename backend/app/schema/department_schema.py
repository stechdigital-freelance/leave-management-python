from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# -----------------------------------
# Base Schema (shared attributes)
# -----------------------------------
class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=255, description="Department name")
    code: Optional[str] = Field(None, max_length=50, description="Unique department code")
    description: Optional[str] = Field(None, description="Department description")
    is_active: Optional[bool] = Field(True, description="Whether the department is active")

# -----------------------------------
# Create Schema (for POST)
# -----------------------------------
class DepartmentCreate(DepartmentBase):
    """Schema for creating a new department"""
    pass  # inherits all fields from base

# -----------------------------------
# Update Schema (for PATCH/PUT)
# -----------------------------------
class DepartmentUpdate(BaseModel):
    """Schema for updating an existing department"""
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(None)

# -----------------------------------
# Read Schema (for GET)
# -----------------------------------
class DepartmentRead(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # works like orm_mode=True (SQLAlchemy → Pydantic)

# -----------------------------------
# Delete Schema (for DELETE)
# -----------------------------------
class DepartmentDelete(BaseModel):
    id: int
    deleted: bool = Field(True, description="Indicates if deletion was successful")

class DepartmentsPublic(BaseModel):
    data: list[DepartmentRead]
    count: int
