from typing import List, Optional
from sqlalchemy.orm import Session

from app.modules.contacts.repository import ContactRepository
from app.modules.contacts.schemas import ContactCreate, ContactUpdate, Contact


class ContactService:
    """Service layer for contact business logic."""
    
    def __init__(self, db: Session):
        self.repository = ContactRepository(db)
    
    def get_contact(self, contact_id: int) -> Optional[Contact]:
        """Get contact by ID."""
        return self.repository.get(contact_id)
    
    def get_contact_by_email(self, email: str) -> Optional[Contact]:
        """Get contact by email."""
        return self.repository.get_by_email(email)
    
    def get_contacts(self, skip: int = 0, limit: int = 100) -> List[Contact]:
        """Get all contacts with pagination."""
        return self.repository.get_all(skip=skip, limit=limit)
    
    def get_contacts_by_company(self, company_id: int, skip: int = 0, limit: int = 100) -> List[Contact]:
        """Get all contacts for a specific company."""
        return self.repository.get_by_company(company_id, skip=skip, limit=limit)
    
    def create_contact(self, contact_data: ContactCreate) -> Contact:
        """Create a new contact."""
        # Check if contact already exists
        if self.repository.get_by_email(contact_data.email):
            raise ValueError("Contact with this email already exists")
        
        return self.repository.create(contact_data)
    
    def update_contact(self, contact_id: int, contact_data: ContactUpdate) -> Optional[Contact]:
        """Update contact."""
        return self.repository.update(contact_id, contact_data)
    
    def delete_contact(self, contact_id: int) -> bool:
        """Delete contact."""
        return self.repository.delete(contact_id)
