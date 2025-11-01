import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ----------------------------------------------------
# Base Model — shared fields
# ----------------------------------------------------
class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    role: str = Field(default="user", pattern="^(user|supervisor|admin|superAdmin)$")


# ----------------------------------------------------
# Create / Register Models
# ----------------------------------------------------
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=40)


class UserRegister(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=40)
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)


# ----------------------------------------------------
# Update Models
# ----------------------------------------------------
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    role: str | None = Field(default=None, pattern="^(user|supervisor|admin|superAdmin)$")


class UserUpdateMe(BaseModel):
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=40)
    new_password: str = Field(..., min_length=8, max_length=40)


# ----------------------------------------------------
# Public Models (response)
# ----------------------------------------------------
class UserPublic(UserBase):
    model_config = {"from_attributes": True}

    id: int                          # database primary key
    user_id: uuid.UUID               # public UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int
