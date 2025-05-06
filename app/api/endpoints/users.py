from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.services.user_service import user_service
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.user import User as UserModel

router = APIRouter()

@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_admin),
) -> Any:
    """
    Retrieve users. Only admin can access this endpoint.
    """
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/me", response_model=User)
def read_user_me(
    current_user: UserModel = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
) -> Any:
    """
    Update own user.
    """
    user = user_service.update_user(db, user_id=current_user.id, user_in=user_in)
    return user

@router.get("/{user_id}", response_model=User)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin),
) -> Any:
    """
    Get a specific user by id. Only admin can access this endpoint.
    """
    user = user_service.get_user(db, user_id=user_id)
    return user

@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_admin),
) -> Any:
    """
    Update a user. Only admin can access this endpoint.
    """
    user = user_service.update_user(db, user_id=user_id, user_in=user_in)
    return user

@router.delete("/{user_id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: UserModel = Depends(get_current_admin),
) -> Any:
    """
    Delete a user. Only admin can access this endpoint.
    """
    user = user_service.delete_user(db, user_id=user_id)
    return user