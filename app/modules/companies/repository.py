from sqlalchemy.orm import Session
from typing import List, Optional

from app.modules.companies.models import Company
from app.modules.companies.schemas import CompanyCreate, CompanyUpdate


class CompanyRepository:
    """Repository for company database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, company_id: int) -> Optional[Company]:
        """Get company by ID."""
        return self.db.query(Company).filter(Company.id == company_id).first()
    
    def get_by_name(self, name: str) -> Optional[Company]:
        """Get company by name."""
        return self.db.query(Company).filter(Company.name == name).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Company]:
        """Get all companies with pagination."""
        return self.db.query(Company).offset(skip).limit(limit).all()
    
    def create(self, company_data: CompanyCreate) -> Company:
        """Create a new company."""
        db_company = Company(**company_data.model_dump())
        self.db.add(db_company)
        self.db.commit()
        self.db.refresh(db_company)
        return db_company
    
    def update(self, company_id: int, company_data: CompanyUpdate) -> Optional[Company]:
        """Update company."""
        db_company = self.get(company_id)
        if not db_company:
            return None
        
        update_data = company_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_company, field, value)
        
        self.db.commit()
        self.db.refresh(db_company)
        return db_company
    
    def delete(self, company_id: int) -> bool:
        """Delete company."""
        db_company = self.get(company_id)
        if not db_company:
            return False
        
        self.db.delete(db_company)
        self.db.commit()
        return True
