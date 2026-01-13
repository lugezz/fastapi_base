from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.contacts.schemas import (
    Contact,
    ContactCreate,
    ContactUpdate,
    ContactWithUser,
)
from app.modules.contacts.service import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


def get_contact_service(db: Session = Depends(get_db)) -> ContactService:
    """Dependency to get contact service."""
    return ContactService(db)


@router.get("/", response_model=List[Contact])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    company_id: int = None,
    service: ContactService = Depends(get_contact_service)
):
    """Get all contacts, optionally filtered by company."""
    if company_id:
        return service.get_contacts_by_company(company_id, skip=skip, limit=limit)
    return service.get_contacts(skip=skip, limit=limit)


@router.get("/{contact_id}", response_model=Contact)
def read_contact(
    contact_id: int,
    service: ContactService = Depends(get_contact_service)
):
    """Get contact by ID."""
    contact = service.get_contact(contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return contact


@router.get("/{contact_id}/with-user", response_model=ContactWithUser)
def read_contact_with_user(
    contact_id: int,
    service: ContactService = Depends(get_contact_service)
):
    """Get contact by ID with user information."""
    contact = service.get_contact(contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return contact


@router.post("/", response_model=Contact, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact_data: ContactCreate,
    service: ContactService = Depends(get_contact_service)
):
    """Create a new contact."""
    try:
        return service.create_contact(contact_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    service: ContactService = Depends(get_contact_service)
):
    """Update contact."""
    contact = service.update_contact(contact_id, contact_data)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    service: ContactService = Depends(get_contact_service)
):
    """Delete contact."""
    if not service.delete_contact(contact_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
