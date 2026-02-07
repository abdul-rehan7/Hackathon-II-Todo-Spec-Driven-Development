from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)


class User(UserBase, table=True):
    """
    User model representing registered users in the system.
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False)  # Stored securely using bcrypt
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str


class UserRead(UserBase):
    """
    Schema for reading user data (without password).
    """
    id: str
    created_at: datetime


class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    email: Optional[str] = None