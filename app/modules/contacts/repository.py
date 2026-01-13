from sqlalchemy.orm import Session
from typing import List, Optional

from app.modules.contacts.models import Contact
from app.modules.contacts.schemas import ContactCreate, ContactUpdate


class ContactRepository:
    """Repository for contact database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, contact_id: int) -> Optional[Contact]:
        """Get contact by ID."""
        return self.db.query(Contact).filter(Contact.id == contact_id).first()
    
    def get_by_email(self, email: str) -> Optional[Contact]:
        """Get contact by email."""
        return self.db.query(Contact).filter(Contact.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Contact]:
        """Get all contacts with pagination."""
        return self.db.query(Contact).offset(skip).limit(limit).all()
    
    def get_by_company(self, company_id: int, skip: int = 0, limit: int = 100) -> List[Contact]:
        """Get all contacts for a specific company."""
        return self.db.query(Contact).filter(
            Contact.company_id == company_id
        ).offset(skip).limit(limit).all()
    
    def create(self, contact_data: ContactCreate) -> Contact:
        """Create a new contact."""
        db_contact = Contact(**contact_data.model_dump())
        self.db.add(db_contact)
        self.db.commit()
        self.db.refresh(db_contact)
        return db_contact
    
    def update(self, contact_id: int, contact_data: ContactUpdate) -> Optional[Contact]:
        """Update contact."""
        db_contact = self.get(contact_id)
        if not db_contact:
            return None
        
        update_data = contact_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_contact, field, value)
        
        self.db.commit()
        self.db.refresh(db_contact)
        return db_contact
    
    def delete(self, contact_id: int) -> bool:
        """Delete contact."""
        db_contact = self.get(contact_id)
        if not db_contact:
            return False
        
        self.db.delete(db_contact)
        self.db.commit()
        return True
