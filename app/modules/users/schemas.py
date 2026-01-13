from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

if TYPE_CHECKING:
    from app.modules.contacts.schemas import Contact


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


class UserBasic(BaseModel):
    """Basic user info for nested responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserInDB(UserBase):
    """Schema for user in database."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class User(UserInDB):
    """Schema for user response."""
    pass


class UserWithContacts(UserInDB):
    """Schema for user response with contacts."""
    contacts: List["Contact"] = []
