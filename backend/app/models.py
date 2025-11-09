import uuid
from sqlalchemy import Boolean, Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, DeclarativeBase
from pydantic import BaseModel, EmailStr, Field


# =========================
# 🧱 SQLAlchemy ORM MODELS
# =========================

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    full_name = Column(String(255), nullable=True)

    items = relationship(
        "Item",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Item(Base):
    __tablename__ = "item"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )

    owner = relationship("User", back_populates="items")


# =========================
# 📦 PYDANTIC SCHEMAS
# =========================

# ----- User Schemas -----
class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    # full_name: str | None = Field(default=None, max_length=255)
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=40)


class UserRegister(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=40)
    new_password: str = Field(..., min_length=8, max_length=40)


class UserPublic(UserBase):
    model_config = {"from_attributes": True}
    id: int


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int

# ----- Item Schemas -----
class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)


class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(BaseModel):
    data: list[ItemPublic]
    count: int


# ----- Auth / Utility Schemas -----
class Message(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None


class NewPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=40)
