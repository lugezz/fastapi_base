from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.users.schemas import User, UserCreate, UserUpdate, UserWithContacts
from app.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency to get user service."""
    return UserService(db)


@router.get("/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service)
):
    """Get all users."""
    return service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Get user by ID."""
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/{user_id}/with-contacts", response_model=UserWithContacts)
def read_user_with_contacts(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Get user by ID with all their contacts."""
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """Create a new user."""
    try:
        return service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    """Update user."""
    user = service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Delete user."""
    if not service.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
