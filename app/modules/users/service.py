from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.users.repository import UserRepository
from app.modules.users.schemas import User, UserCreate, UserUpdate


class UserService:
    """Service layer for user business logic."""

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.repository.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.repository.get_by_email(email)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.repository.get_by_username(username)

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        return self.repository.get_all(skip=skip, limit=limit)

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        if self.repository.get_by_email(user_data.email):
            raise ValueError("Email already registered")

        if self.repository.get_by_username(user_data.username):
            raise ValueError("Username already taken")

        return self.repository.create(user_data)

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user."""
        return self.repository.update(user_id, user_data)

    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        return self.repository.delete(user_id)
