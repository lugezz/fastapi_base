from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Contact(BaseModel):
    """Contact model."""
    __tablename__ = "contacts"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    position = Column(String, nullable=True)

    # Foreign key to company
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    
    # Foreign key to user (owner of this contact)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="contacts")
    # company = relationship("Company", back_populates="contacts")
