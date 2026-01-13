from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.companies.repository import CompanyRepository
from app.modules.companies.schemas import Company, CompanyCreate, CompanyUpdate


class CompanyService:
    """Service layer for company business logic."""

    def __init__(self, db: Session):
        self.repository = CompanyRepository(db)

    def get_company(self, company_id: int) -> Optional[Company]:
        """Get company by ID."""
        return self.repository.get(company_id)

    def get_company_by_name(self, name: str) -> Optional[Company]:
        """Get company by name."""
        return self.repository.get_by_name(name)

    def get_companies(self, skip: int = 0, limit: int = 100) -> List[Company]:
        """Get all companies with pagination."""
        return self.repository.get_all(skip=skip, limit=limit)

    def create_company(self, company_data: CompanyCreate) -> Company:
        """Create a new company."""
        # Check if company already exists
        if self.repository.get_by_name(company_data.name):
            raise ValueError("Company with this name already exists")

        return self.repository.create(company_data)

    def update_company(self, company_id: int, company_data: CompanyUpdate) -> Optional[Company]:
        """Update company."""
        return self.repository.update(company_id, company_data)

    def delete_company(self, company_id: int) -> bool:
        """Delete company."""
        return self.repository.delete(company_id)
