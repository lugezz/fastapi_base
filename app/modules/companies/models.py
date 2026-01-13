from sqlalchemy import Column, String, Text
from app.models.base import BaseModel


class Company(BaseModel):
    """Company model."""
    __tablename__ = "companies"
    
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    website = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
