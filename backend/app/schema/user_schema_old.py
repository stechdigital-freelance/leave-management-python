# app/schemas/user_schema.py
from datetime import datetime
from typing import Optional, Literal, Annotated
import uuid
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
import re


# Constants for validation
USER_ROLES = Literal["user", "supervisor", "admin", "superAdmin"]
NAME_REGEX = r"^[a-zA-ZÀ-ÿ\s\-'.]{2,100}$"


class UserBase(BaseModel):
    """Base schema with common user fields"""
    name: Annotated[
        str, 
        Field(
            min_length=2, 
            max_length=100,
            examples=["John Doe"],
            description="User's full name"
        )
    ]
    email: Annotated[
        EmailStr,
        Field(
            examples=["user@example.com"],
            description="Unique email address"
        )
    ]
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_min_length=1,
        validate_assignment=True,
        extra='forbid'
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name format and clean extra spaces"""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        
        # Clean extra spaces
        cleaned = ' '.join(v.strip().split())
        
        # Check basic format (allow international characters)
        if not re.match(NAME_REGEX, cleaned):
            raise ValueError(
                'Name can only contain letters, spaces, hyphens, apostrophes, and periods'
            )
        
        if len(cleaned) > 100:
            raise ValueError('Name must be less than 100 characters')
            
        return cleaned


class UserCreate(UserBase):
    """Schema for creating new users"""
    # Add password field for creation only
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=128,
            examples=["SecurePassword123!"],
            description="User password (will be hashed before storage)"
        )
    ]

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Basic password strength validation"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # Optional: Add more sophisticated password validation
        if v.lower() in ['password', '12345678', 'qwertyui']:
            raise ValueError('Password is too common')
            
        return v


class UserUpdate(BaseModel):
    """Schema for updating user data - all fields optional"""
    name: Optional[Annotated[
        str, 
        Field(
            min_length=2, 
            max_length=100,
            examples=["John Smith"],
            description="User's full name"
        )
    ]] = None
    
    email: Optional[Annotated[
        EmailStr,
        Field(
            examples=["newemail@example.com"],
            description="Unique email address"
        )
    ]] = None
    
    image: Optional[Annotated[
        str,
        Field(
            max_length=500,
            examples=["https://example.com/avatar.jpg"],
            description="URL to user's profile image"
        )
    ]] = None
    
    role: Optional[Annotated[
        USER_ROLES,
        Field(examples=["user"], description="User role in the system")
    ]] = None
    
    banned: Optional[Annotated[
        bool,
        Field(examples=[False], description="Whether user is banned")
    ]] = None
    
    ban_reason: Optional[Annotated[
        str,
        Field(
            max_length=1000,
            examples=["Violation of terms of service"],
            description="Reason for banning the user"
        )
    ]] = None
    
    ban_expires: Optional[Annotated[
        datetime,
        Field(
            examples=["2024-12-31T23:59:59"],
            description="When the ban expires"
        )
    ]] = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    @field_validator('name', 'email')
    @classmethod
    def validate_optional_fields(cls, v: Optional[str], info) -> Optional[str]:
        """Apply base validations to optional fields when provided"""
        if v is not None:
            if info.field_name == 'name':
                return UserBase.validate_name(v)
        return v


class UserRead(UserBase):
    """Schema for reading user data"""
    id: Annotated[
        int,
        Field(
            examples=[1],
            description="Unique user identifier"
        )
    ]
    email_verified: Annotated[
        bool,
        Field(
            examples=[True],
            description="Whether email has been verified"
        )
    ] = False
    
    image: Optional[Annotated[
        str,
        Field(
            max_length=500,
            examples=["https://example.com/avatar.jpg"],
            description="URL to user's profile image"
        )
    ]] = None
    
    role: Annotated[
        USER_ROLES,
        Field(
            examples=["user"],
            description="User role in the system"
        )
    ] = "user"
    
    banned: Annotated[
        bool,
        Field(
            examples=[False],
            description="Whether user is banned"
        )
    ] = False
    
    ban_reason: Optional[Annotated[
        str,
        Field(
            max_length=1000,
            examples=["Violation of terms of service"],
            description="Reason for banning the user"
        )
    ]] = None
    
    ban_expires: Optional[Annotated[
        datetime,
        Field(
            examples=["2024-12-31T23:59:59"],
            description="When the ban expires"
        )
    ]] = None
    
    created_at: Annotated[
        datetime,
        Field(
            examples=["2024-01-01T00:00:00"],
            description="When the user was created"
        )
    ]
    
    updated_at: Annotated[
        datetime,
        Field(
            examples=["2024-01-01T00:00:00"],
            description="When the user was last updated"
        )
    ]

    model_config = ConfigDict(from_attributes=True)


# Additional specialized read schemas for different use cases
class UserSafeRead(BaseModel):
    """Safe user data for public consumption (no sensitive fields)"""
    id: int
    name: str
    image: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserProfileRead(BaseModel):
    id: uuid.UUID
    name: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool
    email_verified: Optional[bool] = None
    image: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

