"""User Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user.user_model import UserCreate, UserUpdate, UserRegis
from orm_models import User
from app.core.security import hash_password
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticate a user by username and password.

    Args:
        db (Session): The database session.
        username (str): The username of the user.
        password (str): The plain text password.

    Returns:
        User or None: The authenticated user instance if successful, None otherwise.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def get_all_user(db: Session) -> List[User]:
    """
    Retrieve all user records from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[User]: A list of all user instances.
    """
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Retrieve a user record by its ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        Optional[User]: The user instance if found, None otherwise.
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user record in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data to create.

    Returns:
        User: The created user instance.
    """
    new_user_data = user.model_dump()
    new_user_data["password"] = hash_password(new_user_data["password"])
    
    new_user = User(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_register(db: Session, user: UserRegis) -> User:
    """
    Create a new user record for registration in the database.

    Args:
        db (Session): The database session.
        user (UserRegis): The user registration data.

    Returns:
        User: The created user instance.
    """
    new_user_data = user.model_dump()
    new_user_data["password"] = hash_password(new_user_data["password"])
    new_user_data["role"] = "pramusaji" 
    new_user = User(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """
    Update an existing user record.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to update.
        user_update (UserUpdate): The updated user data.

    Returns:
        Optional[User]: The updated user instance if found, None otherwise.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data and update_data["password"] is not None:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> Optional[User]:
    """
    Delete a user record from the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to delete.

    Returns:
        Optional[User]: The deleted user instance if found, None otherwise.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return ("User not found")
    db.delete(user)
    db.commit()
    return user