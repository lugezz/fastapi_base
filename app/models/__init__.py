from app.core.database import Base

# Models are imported directly in alembic/env.py for migrations
# Don't import them here to avoid circular import issues

__all__ = ["Base"]
