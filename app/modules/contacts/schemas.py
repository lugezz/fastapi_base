from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

if TYPE_CHECKING:
    from app.modules.users.schemas import UserBasic


class ContactBase(BaseModel):
    """Base contact schema."""
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    position: Optional[str] = None
    company_id: Optional[int] = None


class ContactCreate(ContactBase):
    """Schema for creating a contact."""
    user_id: int


class ContactUpdate(BaseModel):
    """Schema for updating a contact."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    company_id: Optional[int] = None
    user_id: Optional[int] = None


class ContactInDB(ContactBase):
    """Schema for contact in database."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    full_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class Contact(ContactInDB):
    """Schema for contact response."""
    pass


class ContactWithUser(ContactInDB):
    """Schema for contact response with user information."""
    user: "UserBasic"
