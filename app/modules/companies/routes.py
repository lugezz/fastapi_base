from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.companies.schemas import Company, CompanyCreate, CompanyUpdate
from app.modules.companies.service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


def get_company_service(db: Session = Depends(get_db)) -> CompanyService:
    """Dependency to get company service."""
    return CompanyService(db)


@router.get("/", response_model=List[Company])
def read_companies(
    skip: int = 0,
    limit: int = 100,
    service: CompanyService = Depends(get_company_service)
):
    """Get all companies."""
    return service.get_companies(skip=skip, limit=limit)


@router.get("/{company_id}", response_model=Company)
def read_company(
    company_id: int,
    service: CompanyService = Depends(get_company_service)
):
    """Get company by ID."""
    company = service.get_company(company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    return company


@router.post("/", response_model=Company, status_code=status.HTTP_201_CREATED)
def create_company(
    company_data: CompanyCreate,
    service: CompanyService = Depends(get_company_service)
):
    """Create a new company."""
    try:
        return service.create_company(company_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{company_id}", response_model=Company)
def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    service: CompanyService = Depends(get_company_service)
):
    """Update company."""
    company = service.update_company(company_id, company_data)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: int,
    service: CompanyService = Depends(get_company_service)
):
    """Delete company."""
    if not service.delete_company(company_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
