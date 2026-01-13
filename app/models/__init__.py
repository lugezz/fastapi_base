from app.core.database import Base

# Import all models here to ensure they are registered with Base
# This is important for Alembic migrations
from app.modules.users.models import User
from app.modules.companies.models import Company
from app.modules.contacts.models import Contact

__all__ = ["Base", "User", "Company", "Contact"]
