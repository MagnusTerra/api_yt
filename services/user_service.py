from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from models.user import User as UserModel
from schemas.user import User, UserCreate, UserUpdate
from core.security import get_password_hash

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID"""
    # In a real app, this would query the database
    # For now, return a dummy user
    if user_id == 1:
        return User(
            id=1,
            username="testuser",
            email="test@example.com",
            is_active=True,
            is_superuser=False,
            created_at=datetime.now()
        )
    return None

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get a user by username"""
    # In a real app, this would query the database
    # For now, return a dummy user if username is "testuser"
    if username == "testuser":
        return UserModel(
            id=1,
            username="testuser",
            email="test@example.com",
            is_active=True,
            is_superuser=False,
            created_at=datetime.now(),
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # password: secret
        )
    



def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    db_user = UserModel(
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=datetime.now(),
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    

def update_user(db: Session, user_id: int, user_in: UserUpdate) -> Optional[User]:
    """Update a user"""
    user = get_user(db, user_id)
    if user:
        user.created_at = user.created_at or datetime.now()
    return user

def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
